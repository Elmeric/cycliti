# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import sys
from datetime import datetime, timezone, timedelta

import jwt
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.base_class import Base
import app.config as config
from app.config import Settings
from app import crud
from tests.utils.utils import random_email

# Replace the env file in the settings object
config.settings = Settings(_env_file='/home/eric/code/cycliti/backend/app/app/.test.env')

# All other modules that import settings are imported here
# This ensures that those modules will use the updated settings object
# Don't forget to use "noqa", otherwise a formatter might put it back on top
from app.main import app  # noqa
from app.config import settings
from app.api.deps import get_db # noqa
from app.db.init_db import init_db  # noqa
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def engine():
    url_object = URL.create(
        drivername="mysql+mysqldb",
        username=config.settings.MYSQL_USER,
        password=config.settings.MYSQL_PASSWORD,
        host=config.settings.MYSQL_HOST,
        port=config.settings.MYSQL_PORT,
        database=config.settings.MYSQL_DB,
    )
    engine = create_engine(url_object, pool_pre_ping=True)
    return engine


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest_asyncio.fixture(name="session", scope="session", loop_scope="session")
async def session_fixture(engine, tables):
    """Returns a sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    # session = Session(bind=connection, join_transaction_mode="create_savepoint")
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
        join_transaction_mode="create_savepoint",
    )
    session = session_factory()

    await init_db(session)
    # asyncio.run(init_db(session))

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(name="client", scope="module")
def client_fixture(session: Session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def get_db_override():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


FAKE_TIME = datetime(
    2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def mock_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls, tz=None):
            return FAKE_TIME

    monkeypatch.setattr(
        sys.modules["app.core.security"], "datetime", mydatetime
    )


@pytest.fixture
def mock_create_token_no_sub(monkeypatch):
    def _create_token(subject, expires_delta) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    monkeypatch.setattr(
        sys.modules["app.core.security"], "create_access_token", _create_token
    )


@pytest.fixture
def mock_create_token_unknown_sub(monkeypatch):
    def _create_token(subject, expires_delta) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"exp": expire, "sub": random_email()}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    monkeypatch.setattr(
        sys.modules["app.core.security"], "create_access_token", _create_token
    )


@pytest.fixture
def mock_verify_password_reset_token_unknown_sub(monkeypatch):
    def _verify_token(token) -> str:
        # decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return random_email()

    monkeypatch.setattr(
        sys.modules["app.api.api_v1.endpoints.login"], "verify_password_reset_token", _verify_token
    )


@pytest.fixture
def mock_change_password_commit_failed(monkeypatch):
    async def _change_password(db, user_db, new_password):
        raise crud.CrudError()

    monkeypatch.setattr("app.crud.user.change_password", _change_password)


@pytest.fixture()
def mock_commit(monkeypatch):
    state = {"failed": False}
    called = []

    def _commit(_):
        called.append(True)
        if state["failed"]:
            raise SQLAlchemyError("Commit failed")

    monkeypatch.setattr("app.crud.base.Session.commit", _commit)

    return state, called
