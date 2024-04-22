from datetime import datetime
from typing import Optional
from pydantic import validator

from pydantic import BaseModel, ConfigDict

from ..models.item import ItemTypes, ItemStatus
from ..models.restriction_const import (
    ITEM_TEXT_MAX_LEN,
    ITEM_TEXT_MIN_LEN,
)


class ItemBase(BaseModel):
    item_text: Optional[str]  #  Optional property
    item_type: ItemTypes

    @validator("item_text", pre=True, always=True)
    def check_text_length(cls, v, values, **kwargs):
        if values.get("item_type") == ItemTypes.TEXT:
            if v is None:
                raise ValueError("item_text is required for item type TEXT")
            if len(v) < ITEM_TEXT_MIN_LEN:
                raise ValueError(
                    "Text can't be shorter than {ITEM_TEXT_MIN_LEN} characters"
                )
            if len(v) > ITEM_TEXT_MAX_LEN:
                raise ValueError(
                    "Text can't be longer than {ITEM_TEXT_MAX_LEN} characters"
                )
        return v


class ItemSchema(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_type: ItemTypes
    created_at: datetime
    status: ItemStatus


# response
class ItemOut(ItemSchema):
    pass
