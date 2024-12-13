# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from datetime import UTC
from datetime import datetime as dt
from typing import Annotated

import requests
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic_core import Url
from sqlalchemy.orm import Session

import crud
from app.api import deps
from config import settings

router = APIRouter()


@router.get(
    "/link",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def link_to_strava(
    state: str,
    code: str,
    scope: str,
    db: Annotated[Session, Depends(deps.get_db)],
):
    """
    Get access and refresh tokens from Strava.
    """
    # Check that accepted scope complies with the requested one
    accepted_scope = scope.split(",")
    scope_ok = True
    for s in "read,read_all,profile:read_all,activity:read,activity:read_all".split(","):
        if s not in accepted_scope:
            scope_ok = False
            break
    if not scope_ok:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Incorrect scope: you shall accept the required authorizations.",
        )

    # Define the payload
    payload = {
        "client_id": settings.STRAVA_CLIENT_ID,
        "client_secret": settings.STRAVA_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }

    try:
        # Send a POST request to the Strava token URL
        response = requests.post(settings.STRAVA_TOKEN_URL, data=payload)

        # Check if the response status code is not 200
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to retrieve tokens from Strava",
            )

        # Get the tokens from the response
        # https://developers.strava.com/docs/reference/#api-models-SummaryAthlete
        token_response = response.json()
        access_token: str = token_response["access_token"]
        refresh_token:str = token_response["refresh_token"]
        expires_at: int = token_response["expires_at"]
        print(f"Access token: {access_token}")
        print(f"Refresh token: {refresh_token}")
        print(f"Expires at: {dt.fromtimestamp(expires_at, UTC)}")
        # {
        #     'token_type': 'Bearer',
        #      'expires_at': 1733278049,
        #      'expires_in': 20538,
        #      'refresh_token': '66fda821efc3570e78f20d1edab4577e2032b614',
        #      'access_token': '7226114bd212ce665cf3c6f89b7825dd20c7ab58',
        #      'athlete': {
        #          'id': 35484046,
        #          'username': None,
        #          'resource_state': 2,
        #          'firstname': 'Eric',
        #          'lastname': 'Lemoine',
        #          'bio': '',
        #          'city': '',
        #          'state': '',
        #          'country': None,
        #          'sex': 'M',
        #          'premium': True,
        #          'summit': True,
        #          'created_at': '2018-10-06T14:02:17Z',
        #          'updated_at': '2024-03-20T19:10:24Z',
        #          'badge_type_id': 1,
        #          'weight': 70.0,
        #          'profile_medium': 'https://lh3.googleusercontent.com/a/ACg8ocImx8xhxTIR6OvxnqwOAf47DDZdMZKClLMxaqstROtbRvmMgx8=s96-c',
        #          'profile': 'https://lh3.googleusercontent.com/a/ACg8ocImx8xhxTIR6OvxnqwOAf47DDZdMZKClLMxaqstROtbRvmMgx8=s96-c',
        #          'friend': None,
        #          'follower': None
        #      }
        #  }

        # Retrieve the user by the provided state (user id)
        user = await crud.user.get(db, obj_id=int(state))

        # Check that it is an active user
        if not crud.user.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource.",
            )

        # Update the user's strava_link with the response tokens
        await crud.user.link_to_strava(
            db, db_obj=user, tokens=(access_token, refresh_token, expires_at)
        )

        # Redirect to the main page or any other desired page after processing
        redirect_url = Url(str(settings.FRONTEND_HOST) + "?stravaLinked=1")
            # "https://" + settings.FRONTEND_HOST + "/settings?stravaLinked=1"
        print(redirect_url)

        # Return a RedirectResponse to the redirect URL
        return redirect_url
    except Exception as err:
        # Log the exception
        # logger.error(f"Error in strava_link: {err}", exc_info=True)
        print(err)

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occur, please retry.",
        )
