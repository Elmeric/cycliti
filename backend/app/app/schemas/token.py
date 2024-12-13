from typing import Optional

from pydantic import BaseModel

from app.schemas import User


class Token(BaseModel):
    access_token: str
    token_type: str


class UserToken(BaseModel):
    user: User
    token: Token


class TokenPayload(BaseModel):
    sub: Optional[str] = None
