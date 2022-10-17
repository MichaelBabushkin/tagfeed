from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr

from .tag import TagCreate
from ..models.item import ItemTypes
from ..models.restriction_const import (
    ITEM_CONTENT_MIN_LEN,
    ITEM_CONTENT_MAX_LEN,
    ITEM_PREVIEW_MAX_LEN,
)


class ItemBase(BaseModel):
    item_type: ItemTypes  # Required property
    content: constr(
        min_length=ITEM_CONTENT_MIN_LEN, max_length=ITEM_CONTENT_MAX_LEN
    )  # Required property
    preview: Optional[constr(max_length=ITEM_PREVIEW_MAX_LEN)]  #  Optional property


class ItemCreate(ItemBase):
    pass


class ItemSchema(ItemBase):
    id: int
    created_at: datetime

    class Config:  # Allows fastapi to work with orm models instead of dicts
        orm_mode = True


# response
class ItemOut(ItemSchema):
    pass
