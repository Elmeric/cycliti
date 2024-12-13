from datetime import timedelta
from typing import Any, Annotated, Union

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.config import settings
from app.utils import (
    send_reset_password_email,
    verify_password_reset_nonce,
)

router = APIRouter()


# https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-and-error-messages
@router.post(
    "/login/access-token",
    response_model=schemas.UserToken,
)
async def get_access_token(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
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
    # TODO: return exception (Locked user) if user.login_failed counter exceeds a thredhold (3)
    # elif user.login_failed >= 3:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You're locked out of the system due to too many attempts. Contact your admin.."
    #     )
    # Login success: reset any pending reset password requests
    try:
        await crud.user.reset_password_reset(db, db_obj=user)
    except crud.CrudError:
        # TODO: Log the error
        print(f"Login succes for user: {user.email} but cannot reset "
              f"its password_reset entry")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = schemas.Token(
        access_token=security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )
    return schemas.UserToken(user=user, token=token)


@router.post("/login/test-token", response_model=schemas.User)
def test_token(
        current_user: models.User = Depends(deps.get_current_user)
) -> models.User:
    """
    Test access token
    """
    return current_user


@router.post("/forgot-password/{email}", response_model=schemas.Msg)
async def forgot_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)

    if user:
        if password_reset := user.password_reset:
            # A previous password reset attempt exists
            if (attemps := password_reset.attempts) < settings.PASSWORD_RECOVERY_MAX_ATTEMPTS:
                # Max attempts not reached, update the password reset table
                try:
                    user = await crud.user.update_password_reset(
                        db, db_obj=user, attempts=attemps + 1
                    )
                except crud.CrudError:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"An error occur, please retry."
                    )
            else:   # Max attempts reached: return a Bad Request status
                # TODO: Lock the user for at least 24 hours
                # TODO: Add a background task that reset password reset older than 24 hours
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You don't have permission to access this resource."
                )
        else:   # First attempt: create a password reset entry
            try:
                user = await crud.user.create_password_reset(db, db_obj=user)
            except crud.CrudError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An error occur, please retry."
                )
        print(f"Reset password nonce: {user.password_reset.nonce}")
        send_reset_password_email(
            email_to=user.email, email=email, nonce=user.password_reset.nonce
        )
    return {
        "msg": "If there is a Cycliti account associated with the address "
               "you provided, we will send you an e-mail with instructions "
               "on how to reset your password."
    }


@router.post("/reset-password/", response_model=schemas.Msg)
async def reset_password(
    email: Annotated[str, Body()],
    new_password: Annotated[str, Body()],
    nonce: Annotated[str, Body()],
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password reset failed; Invalid user ID or token.",
    )
    user = await crud.user.get_by_email(db, email=email)
    if not user or not crud.user.is_active(user):
        raise credentials_exception
    if not user.password_reset:
        raise credentials_exception
    expected_nonce = user.password_reset.nonce
    issued_at = user.password_reset.issued_at
    valid = verify_password_reset_nonce(nonce, expected_nonce, issued_at)
    if not valid:
        raise credentials_exception
    try:
        await crud.user.change_password(
            db, user_db=user, new_password=new_password, reset=True
        )
    except (crud.CrudError, Exception) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occur, please retry."
        )
    return {"msg": "Password updated successfully."}
