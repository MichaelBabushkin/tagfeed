from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated, Optional

from .restriction_const import (
    ACCESS_TOKEN_MIN_LEN,
    ACCESS_TOKEN_MAX_LEN,
    TOKEN_TYPE_MIN_LEN,
    TOKEN_TYPE_MAX_LEN,
)


class Token(BaseModel):
    access_token: Annotated[
        str,
        StringConstraints(
            min_length=ACCESS_TOKEN_MIN_LEN, max_length=ACCESS_TOKEN_MAX_LEN
        ),
    ]  # Required property
    token_type: Annotated[
        str,
        StringConstraints(min_length=TOKEN_TYPE_MIN_LEN, max_length=TOKEN_TYPE_MAX_LEN),
    ]  # Required property


class TokenData(BaseModel):
    username: Optional[str] = None
