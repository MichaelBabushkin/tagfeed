from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

from ..models.restriction_const import (
    TAG_NAME_MIN_LEN,
    TAG_NAME_MAX_LEN,
)


class TagBase(BaseModel):
    name: Annotated[
        str, StringConstraints(min_length=TAG_NAME_MIN_LEN, max_length=TAG_NAME_MAX_LEN)
    ]  # Required property


class TagCreate(TagBase):
    pass


class TagSchema(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


# response
class TagOut(TagSchema):
    pass
