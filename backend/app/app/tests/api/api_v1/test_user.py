import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from argon2 import PasswordHasher

from app import crud
from app.core.security import verify_password
# from app.schemas.user import UserCreate, UserUpdate
# from app.tests.utils.utils import random_email, random_lower_string
from app import schemas
from config import settings
from app.db.init_db import init_db  # noqa


def test_create_user(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "titi.toto@free.fr",
            "username": "Titi",
            "password": "password",
        }
    )
    assert response.status_code is status.HTTP_201_CREATED
    msg = response.json()
    assert "msg" in msg
    assert msg["msg"] == ("A link to activate your account has been emailed "
                          "to the address you provided.")


def test_create_user_same_email(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "moi.nous@eux.fr",
            "username": "Moi",
            "password": "password",
        }
    )
    assert response.status_code is status.HTTP_201_CREATED

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "moi.nous@eux.fr",
            "username": "Toto",
            "password": "passw0rd",
        }
    )
    assert r.status_code is status.HTTP_400_BAD_REQUEST
    assert "An error occur, please retry." in r.text


def test_create_user_same_username(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "a.a@free.fr",
            "username": "Aaa",
            "password": "password",
        }
    )
    assert response.status_code is status.HTTP_201_CREATED

    r = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "b.b@free.fr",
            "username": "Aaa",
            "password": "passw0rd",
        }
    )
    assert response.status_code is status.HTTP_201_CREATED
    msg = response.json()
    assert "msg" in msg
    assert msg["msg"] == ("A link to activate your account has been emailed "
                          "to the address you provided.")


# def test_create_user_error(client: TestClient, mock_commit):
#     state, _called = mock_commit
#     state["failed"] = True
#
#     # with pytest.raises(HTTPException):
#     response = client.post(
#         "/users/",
#         json={
#             "email": "titi.toto@free.fr",
#             "name": "Titi Toto",
#             "username": "Titi",
#         }
#     )
#     assert response.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR
