from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from core.security import verify_password
from schemas import UserCreate
from tests.utils.utils import random_email, random_lower_string


#
# Path: /login/access-token
#
def test_get_access_token_success(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_USER_EMAIL,
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_invalid_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_USER_EMAIL,
        "password": random_lower_string(32),
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
    assert "Login failed; Invalid user ID or password" in r.text


def test_get_access_token_unknown_user(client: TestClient) -> None:
    login_data = {
        "username": random_email(),
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
    assert "Login failed; Invalid user ID or password" in r.text


async def test_get_access_token_inactive_user(session: Session, client: TestClient) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)

    login_data = {
        "username": user.email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
    assert "Login failed; Invalid user ID or password" in r.text


#
# Path: /login/test-token
#
def test_use_access_token_success(
    client: TestClient, first_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=first_user_token_headers,
    )
    assert r.status_code == 200
    result = r.json()
    assert "email" in result


def test_use_access_token_no_sub_claim(
    client: TestClient,
        mock_create_token_no_sub,
        first_user_token_headers: dict[str, str],
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=first_user_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_use_access_token_expired_token(
    client: TestClient, mock_datetime_now, first_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=first_user_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_use_access_token_unknowk_user(
        client: TestClient,
        mock_create_token_unknown_sub,
        first_user_token_headers: dict[str, str],
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=first_user_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


#
# Path: /password-recovery/{email}
#
def test_forgot_password_four_attempts(client: TestClient) -> None:
    # First attempt
    email = settings.FIRST_USER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith(
        "If there is a Cycliti account associated with the address you provided, "
        "we will send you an e-mail with instructions on how to reset your password."
    )
    # Second attempt
    email = settings.FIRST_USER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith(
        "If there is a Cycliti account associated with the address you provided, "
        "we will send you an e-mail with instructions on how to reset your password."
    )
    # Third attempts
    email = settings.FIRST_USER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith(
        "If there is a Cycliti account associated with the address you provided, "
        "we will send you an e-mail with instructions on how to reset your password."
    )
    # Fourth attempts, failed
    email = settings.FIRST_USER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_forgot_password_unknown_user(client: TestClient) -> None:
    email = random_email()
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith(
        "If there is a Cycliti account associated with the address you provided, "
        "we will send you an e-mail with instructions on how to reset your password."
    )


#
# Path: /reset-password
#
async def test_reset_password_success(
        client: TestClient, mock_generate_nonce, session: Session
) -> None:
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
    assert user.is_active
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    body_data = {
        "email": email,
        "new_password": "ericeric",
        "nonce": "NONCE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"] == "Password updated successfully."
    user = await crud.user.get_by_email(session, email=email)
    assert verify_password("ericeric", user.hashed_password)


async def test_reset_password_unknown_user(
        client: TestClient, mock_generate_nonce, session: Session
) -> None:
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
    assert user.is_active
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    body_data = {
        "email": random_email(),
        "new_password": "ericeric",
        "nonce": "NONCE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 400
    assert "Password reset failed; Invalid user ID or token." in r.text


async def test_reset_password_inactive_user(
        session: Session, client: TestClient, mock_generate_nonce
) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
        is_active=False,
    )
    user = await crud.user.create(session, obj_in=user_in)
    assert not user.is_active

    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200

    body_data = {
        "email": email,
        "new_password": "changeme",
        "nonce": "NONCE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 400
    assert "Password reset failed; Invalid user ID or token." in r.text


async def test_reset_password_no_password_reset(
        client: TestClient, mock_generate_nonce, session: Session
) -> None:
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
    assert not user.password_reset
    body_data = {
        "email": email,
        "new_password": "ericeric",
        "nonce": "NONCE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 400
    assert "Password reset failed; Invalid user ID or token." in r.text


async def test_reset_password_invalid_nonce(
        client: TestClient, session: Session
) -> None:
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
    assert user.is_active
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    body_data = {
        "email": email,
        "new_password": "ericeric",
        "nonce": "FAKE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 400
    assert "Password reset failed; Invalid user ID or token." in r.text


async def test_reset_password_db_server_error(
        session:Session,
        client: TestClient,
        mock_change_password_commit_failed,
        mock_generate_nonce,
) -> None:
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
    assert user.is_active
    r = client.post(f"{settings.API_V1_STR}/forgot-password/{email}")
    assert r.status_code == 200
    body_data = {
        "email": email,
        "new_password": "ericeric",
        "nonce": "NONCE",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 500
    assert "An error occur, please retry." in r.text
