# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from enum import IntEnum

from pydantic import BaseModel, EmailStr, ConfigDict, Field, SecretStr, UUID4, PositiveInt, DirectoryPath, PastDate


class GenderEnum(IntEnum):
    male = 1
    female = 2


# https://stackoverflow.com/questions/72214347/how-to-document-default-none-null-in-openapi-swagger-using-fastapi/72289969#72289969
# https://docs.pydantic.dev/latest/concepts/json_schema/#skipjsonschema-annotation
# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(max_length=16)
    is_active: bool = False


# Properties to receive via API on creation
# class UserCreate(BaseModel):
class UserCreate(UserBase):
    # email: EmailStr
    # username: str = Field(max_length=16)
    password: SecretStr = Field(min_length=8, max_length=64)
    # is_active: bool = False


# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None)
    username: str | None = Field(max_length=16, default=None)
    password: SecretStr | None = Field(min_length=8, max_length=64, default=None)
    name: str | None = Field(max_length=64, default=None)
    city: str | None = Field(max_length=64, default=None)
    birthdate: PastDate | None = Field(default=None)
    gender: GenderEnum | None = Field(default=None)
    photo_path: DirectoryPath | None = Field(default=None)
    preferred_language: str | None = Field(default=None)
    access_type: int | None = Field(default=None)

    # model_config = ConfigDict(from_attributes=True)


# class _UserInDBBase(_UserBase):
#     id: int | None = None
#
#     model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
# class User(BaseModel):
class User(UserBase):
    id: PositiveInt
    # uid: UUID4
    # hashed_password: str
    # email: EmailStr
    # username: str = Field(max_length=16)
    name: str | None = Field(max_length=64)
    city: str | None = Field(max_length=64)
    birthdate: PastDate | None
    gender: GenderEnum | None
    photo_path: DirectoryPath | None
    preferred_language: str
    access_type: int
    # is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Additional properties stored in DB
class UserInDB(User):
    uid: UUID4
    hashed_password: str

    # model_config = ConfigDict(from_attributes=True)
