from pydantic import BaseModel, EmailStr, constr

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


class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=USER_USERNAME_MIN_LEN, max_length=USER_USERNAME_MAX_LEN)
    password: constr(min_length=USER_PASSWORD_MIN_LEN, max_length=USER_PASSWORD_MAX_LEN)
    first_name: constr(
        min_length=USER_FIRST_NAME_MIN_LEN, max_length=USER_FIRST_NAME_MAX_LEN
    )
    last_name: constr(
        min_length=USER_LAST_NAME_MIN_LEN, max_length=USER_LAST_NAME_MAX_LEN
    )


class UserOut(BaseModel):
    email: EmailStr
    username: constr(min_length=USER_USERNAME_MIN_LEN, max_length=USER_USERNAME_MAX_LEN)
    first_name: constr(
        min_length=USER_FIRST_NAME_MIN_LEN, max_length=USER_FIRST_NAME_MAX_LEN
    )
    last_name: constr(
        min_length=USER_LAST_NAME_MIN_LEN, max_length=USER_LAST_NAME_MAX_LEN
    )

    class Config:  # Allows fastapi to work with orm models instead of dicts
        orm_mode = True
