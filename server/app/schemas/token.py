from pydantic import BaseModel, constr
from typing import Optional

from .restriction_const import (
    ACCESS_TOKEN_MIN_LEN,
    ACCESS_TOKEN_MAX_LEN,
    TOKEN_TYPE_MIN_LEN,
    TOKEN_TYPE_MAX_LEN,
)


class Token(BaseModel):
    access_token: constr(
        min_length=ACCESS_TOKEN_MIN_LEN, max_length=ACCESS_TOKEN_MAX_LEN
    )
    token_type: constr(min_length=TOKEN_TYPE_MIN_LEN, max_length=TOKEN_TYPE_MAX_LEN)


class TokenData(BaseModel):
    username: Optional[str] = None
