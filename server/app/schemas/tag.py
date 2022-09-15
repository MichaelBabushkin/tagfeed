from pydantic import BaseModel, constr

from ..models.restriction_const import (
    TAG_NAME_MIN_LEN,
    TAG_NAME_MAX_LEN,
)


class TagBase(BaseModel):
    name: constr(
        min_length=TAG_NAME_MIN_LEN, max_length=TAG_NAME_MAX_LEN
    )  # Required property


class TagCreate(TagBase):
    pass


class TagSchema(TagBase):
    id: int
    user_id: int

    class Config:  # Allows fastapi to work with orm models instead of dicts
        orm_mode = True


# response
class TagOut(TagSchema):
    pass
