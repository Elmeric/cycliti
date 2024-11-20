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
    # assert response.text is ""
    assert response.status_code is status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    # assert data["uid"] is not None
    assert data["email"] == "titi.toto@free.fr"
    assert data["username"] == "Titi"
    # assert security.verify_password("password", data["hashed_pwd"]) is True
    assert data["name"] is None
    assert data["city"] is None
    assert data["birthdate"] is None
    assert data["preferred_language"] == "fr-FR"
    assert data["gender"] is None
    assert data["access_type"] == 1
    assert data["photo_path"] is None
    assert data["is_active"] is False
    assert data["is_superuser"] is False


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
