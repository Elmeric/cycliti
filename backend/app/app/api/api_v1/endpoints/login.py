from datetime import timedelta
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.config import settings
from app.utils import (
    generate_nonce,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


# https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-and-error-messages
@router.post("/login/access-token", response_model=schemas.Token)
async def get_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login failed; Invalid user ID or password."
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login failed; Invalid user ID or password."
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.Token(
        access_token=security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )


@router.post("/login/test-token", response_model=schemas.User)
def test_token(
        current_user: models.User = Depends(deps.get_current_user)
) -> models.User:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)

    if user:
        password_reset_token = generate_nonce()
        send_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
    return {"msg": "If that email address is in our database, "
                   "we will send you an email to reset your password."}


@router.post("/reset-password/", response_model=schemas.Msg)
async def reset_password(
    token: Annotated[str, Body()],
    new_password: Annotated[str, Body()],
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this resource.",
    )
    email = verify_password_reset_token(token)
    if not email:
        raise credentials_exception
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise credentials_exception
    elif not crud.user.is_active(user):
        raise credentials_exception
    try:
        await crud.user.change_password(db, user_db=user, new_password=new_password)
    except (crud.CrudError, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occur, please retry."
        )
    return {"msg": "Password updated successfully."}
