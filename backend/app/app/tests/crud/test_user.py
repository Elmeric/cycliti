import pytest
from fastapi.encoders import jsonable_encoder
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from config import settings
from crud import CrudError


async def test_init_db(session: Session):
    user = await crud.user.get_by_email(session, email=settings.FIRST_SUPERUSER_EMAIL)
    assert user is not None
    assert user.username == settings.FIRST_SUPERUSER_USERNAME
    assert user.is_active
    assert user.is_superuser


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
    assert not user.is_superuser
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


async def test_check_if_user_is_active(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
        is_active=True,
    )
    user = await crud.user.create(session, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


async def test_check_if_user_is_active_inactive(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is False


async def test_check_if_user_is_superuser(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
        is_superuser=True,
    )
    user = await crud.user.create(session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


async def test_check_if_user_is_superuser_normal_user(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


async def test_get_user(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)
    user_2 = await crud.user.get(session, obj_id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert user.username == user_2.username


async def test_get_user_unknown_user(session: Session) -> None:
    user = await crud.user.get(session, obj_id=42)
    assert user is None


async def test_activate_user(session: Session) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)
    assert not user.is_active
    await crud.user.activate(session, db_obj=user)
    activated_user = await crud.user.get(session, user.id)
    assert activated_user.is_active
    assert activated_user.activation is None


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
