from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints
from typing_extensions import Annotated

from ..models.restriction_const import (
    USER_PASSWORD_MIN_LEN,
    USER_PASSWORD_MAX_LEN,
    USER_USERNAME_MIN_LEN,
    USER_USERNAME_MAX_LEN,
    USER_FIRST_NAME_MIN_LEN,
    USER_FIRST_NAME_MAX_LEN,
    USER_LAST_NAME_MIN_LEN,
    USER_LAST_NAME_MAX_LEN,
)

class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, StringConstraints(
        min_length=USER_USERNAME_MIN_LEN, max_length=USER_USERNAME_MAX_LEN
    )]
    first_name: Annotated[str, StringConstraints(
        min_length=USER_FIRST_NAME_MIN_LEN, max_length=USER_FIRST_NAME_MAX_LEN
    )]
    last_name: Annotated[str, StringConstraints(
        min_length=USER_LAST_NAME_MIN_LEN, max_length=USER_LAST_NAME_MAX_LEN
    )]


class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(
        min_length=USER_PASSWORD_MIN_LEN, max_length=USER_PASSWORD_MAX_LEN
    )]


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

