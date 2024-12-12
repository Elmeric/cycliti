import pytest
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from config import settings


async def test_init_db(session: Session):
    user = await crud.user.get_by_email(session, email=settings.FIRST_USER_EMAIL)
    assert user is not None
    assert user.username == settings.FIRST_USER_USERNAME
    assert user.is_active


async def test_create_user(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = SecretStr(random_lower_string(32))
    user_in = UserCreate(email=email, username=username, password=password)
    user = await crud.user.create(session, obj_in=user_in)
    assert user.email == email
    assert user.username == username
    assert hasattr(user, "hashed_password")
    assert not user.is_active
    assert user.activation.nonce
    assert user.activation.issued_at
    assert user.activation.user_id == user.id


async def test_authenticate_user(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(email=email, username=username, password=SecretStr(password))
    user = await crud.user.create(session, obj_in=user_in)
    authenticated_user = await crud.user.authenticate(
        session, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email
    assert user.username == authenticated_user.username


async def test_not_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user = await crud.user.authenticate(session, email=email, password=password)
    assert user is None


async def test_check_if_user_is_active(
        session: Session, random_active_user
) -> None:
    is_active = crud.user.is_active(random_active_user)
    assert is_active is True


async def test_check_if_user_is_active_inactive(
        session: Session, random_user
) -> None:
    is_active = crud.user.is_active(random_user)
    assert is_active is False


async def test_get_user(session: Session, random_user) -> None:
    user = random_user
    user_2 = await crud.user.get(session, obj_id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert user.username == user_2.username


async def test_get_user_unknown_user(session: Session) -> None:
    user = await crud.user.get(session, obj_id=42)
    assert user is None


async def test_activate_user(session: Session, random_user) -> None:
    user = random_user
    assert not user.is_active
    await crud.user.activate(session, db_obj=user)
    activated_user = await crud.user.get(session, user.id)
    assert activated_user.is_active
    assert activated_user.activation is None


async def test_link_to_strava_success(session: Session, random_active_user) -> None:
    await crud.user.link_to_strava(
        session, db_obj=random_active_user, tokens=("access", "refresh", 12345)
    )
    linked_user = await crud.user.get(session, random_active_user.id)
    assert linked_user.strava_link.access_token == "access"
    assert linked_user.strava_link.refresh_token == "refresh"
    assert linked_user.strava_link.expires_at == 12345


async def test_link_to_strava_commit_failed(
        session: Session, random_active_user, mock_commit
) -> None:
    state, called = mock_commit
    state["failed"] = True

    with pytest.raises(crud.CrudError):
        await crud.user.link_to_strava(
            session, db_obj=random_active_user, tokens=("access", "refresh", 12345)
        )
    assert called[0]


# def test_update_user(db: Session) -> None:
#     password = random_lower_string()
#     email = random_email()
#     user_in = UserCreate(email=email, password=password, is_superuser=True)
#     user = crud.user.create(db, obj_in=user_in)
#     new_password = random_lower_string()
#     user_in_update = UserUpdate(password=new_password, is_superuser=True)
#     crud.user.update(db, db_obj=user, obj_in=user_in_update)
#     user_2 = crud.user.get(db, id=user.id)
#     assert user_2
#     assert user.email == user_2.email
#     assert verify_password(new_password, user_2.hashed_password)
