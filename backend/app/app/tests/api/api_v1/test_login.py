import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from schemas import UserCreate
from tests.utils.utils import random_email, random_lower_string
from utils import generate_nonce


#
# Path: /login/access-token
#
def test_get_access_token_success(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_invalid_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": random_lower_string(32),
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400
    assert "Login failed; Invalid user ID or password" in r.text


def test_get_access_token_unknown_user(client: TestClient) -> None:
    login_data = {
        "username": random_email(),
        "password": settings.FIRST_SUPERUSER_PASSWORD,
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
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    result = r.json()
    assert "email" in result


def test_use_access_token_no_sub_claim(
    client: TestClient,
        mock_create_token_no_sub,
        superuser_token_headers: dict[str, str],
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_use_access_token_expired_token(
    client: TestClient, mock_datetime_now, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_use_access_token_unknowk_user(
        client: TestClient,
        mock_create_token_unknown_sub,
        superuser_token_headers: dict[str, str],
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


#
# Path: /password-recovery/{email}
#
def test_recover_password_success(client: TestClient) -> None:
    email = settings.FIRST_SUPERUSER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith("If that email address is in our database, "
                                 "we will send you an email to reset your password.")


def test_recover_password_unknown_user(client: TestClient) -> None:
    email = random_email()
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"].startswith("If that email address is in our database, "
                                 "we will send you an email to reset your password.")


#
# Path: /reset-password
#
def test_reset_password_success(client: TestClient) -> None:
    email = settings.FIRST_SUPERUSER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    token = generate_nonce()
    body_data = {
        "token": token,
        "new_password": "ericeric",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 200
    msg = r.json()
    assert "msg" in msg
    assert msg["msg"] == "Password updated successfully."


def test_reset_password_invalid_token(client: TestClient) -> None:
    body_data = {
        "token": random_lower_string(32),
        "new_password": random_lower_string(8),
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 403
    assert "You don't have permission to access this resource" in r.text


def test_reset_password_unknown_user(
        client: TestClient,
        mock_verify_password_reset_token_unknown_sub
) -> None:
    email = settings.FIRST_SUPERUSER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    token = generate_nonce()
    body_data = {
        "token": token,
        "new_password": "ericeric",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 403
    assert "You don't have permission to access this resource." in r.text


async def test_reset_password_inactive_user(session: Session, client: TestClient) -> None:
    email = random_email()
    username = random_lower_string(8)
    password = random_lower_string(32)
    user_in = UserCreate(
        email=email,
        username=username,
        password=SecretStr(password),
    )
    user = await crud.user.create(session, obj_in=user_in)

    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    token = generate_nonce()
    body_data = {
        "token": token,
        "new_password": "changeme",
    }

    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 403
    assert f"You don't have permission to access this resource" in r.text


def test_reset_password_db_server_error(
        session: Session,
        client: TestClient,
        mock_change_password_commit_failed,
) -> None:
    email = settings.FIRST_SUPERUSER_EMAIL
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}")
    assert r.status_code == 200
    token = generate_nonce()
    body_data = {
        "token": token,
        "new_password": "ericeric",
    }
    r = client.post(f"{settings.API_V1_STR}/reset-password/", json=body_data)
    assert r.status_code == 500
    assert "An error occur, please retry." in r.text
