# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from fastapi import APIRouter

import api.api_v1.endpoints.users as users_router

router = APIRouter()


@router.get("/")
async def root():
    return {"messages": "Hello world"}


router.include_router(
    users_router.router,
    prefix="/users",
    tags=["users"],
)
