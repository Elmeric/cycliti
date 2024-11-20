# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import Any
from uuid import uuid4

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from schemas import UserInDB

# from crud.base import CrudError


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.User],
)
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> list[schemas.User]:
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> models.User:
    """
    Create new user.
    """
    same_email = await crud.user.get_by_email(db, email=user_in.email)
    same_username = await crud.user.get_by_username(db, username=user_in.username)
    if same_email or same_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system.",
        )
    try:
        user = await crud.user.create(db, obj_in=user_in)
    except crud.CrudError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal database server error."
        )
    # try:
    #     user = schemas.User.model_validate(user)
    # except ValidationError as exc:
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail=f"User model validation error: {exc}"
    #     )
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> schemas.User:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, obj_id=user_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return user
