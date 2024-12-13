import random
import string
from time import sleep

from fastapi.testclient import TestClient

from app.config import settings


def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_first_user_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_USER_EMAIL,
        "password": settings.FIRST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    user_token = r.json()
    token = user_token["token"]
    a_token = token["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
