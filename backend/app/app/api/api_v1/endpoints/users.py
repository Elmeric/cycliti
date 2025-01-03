# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import Any, Annotated

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from utils import (
    send_account_activation_email,
    verify_account_activation_nonce,
)


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
    response_model=schemas.Msg,
)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    same_email = await crud.user.get_by_email(db, email=user_in.email)
    if same_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occur, please retry.",
        )
    try:
        user = await crud.user.create(db, obj_in=user_in)
    except crud.CrudError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occur, please retry."
        )
    send_account_activation_email(
        email_to=user.email, email=user_in.email, nonce=user.activation.nonce
    )
    return {"msg": "A link to activate your account has been emailed "
                   "to the address you provided."}


@router.post(
    "/resend-activation-email",
    response_model=schemas.Msg,
)
async def resend_activation_email(
    *,
    email: Annotated[str, Body()],
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Resend an activation email to the provided email if exist and allowed.
    """
    user = await crud.user.get_by_email(db, email=email)
    if not user or crud.user.is_active(user) or not user.activation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource.",
    )
    try:
        user = await crud.user.update_activation(db, db_obj=user)
    except crud.CrudError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occur, please retry."
        )
    send_account_activation_email(
        email_to=user.email, email=email, nonce=user.activation.nonce
    )
    return {"msg": "A link to activate your account has been emailed "
                   "to the address provided."}


@router.post("/activate-account", response_model=schemas.Msg)
async def activate_account(
    email: Annotated[str, Body()],
    nonce: Annotated[str, Body()],
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this resource.",
    )
    print(f"Email: {email}")
    print(f"Nonce: {nonce}")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise credentials_exception
    print(f"User: {user}")
    if crud.user.is_active(user):
        return {"msg": "Your account is activated: Log in and enjoy Cycliti!"}
    expected_nonce = user.activation.nonce
    issued_at = user.activation.issued_at
    print(f"Expected nonce: {expected_nonce}")
    print(f"Issued at: {issued_at}")
    valid = verify_account_activation_nonce(nonce, expected_nonce, issued_at)
    if not valid:
        raise credentials_exception
    try:
        await crud.user.activate(db, db_obj=user)
    except crud.CrudError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occur, please retry."
        )
    return {"msg": "Your account is activated. Log in and enjoy Cycliti!"}


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
