from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo

from ..models.item import ItemTypes, ItemStatus
from ..models.restriction_const import (
    ITEM_TEXT_MAX_LEN,
    ITEM_TEXT_MIN_LEN,
)

class ItemBase(BaseModel):
    item_text: Optional[str]  #  Optional property
    item_type: ItemTypes
    @field_validator("item_type")
    def content_length_validator(cls, v, info: ValidationInfo):
        if v is ItemTypes.TEXT:
            k = "item_text"
            if not k in info.data:
                raise ValueError(f"For item_type {v.name}, text must exist")
            if len(info.data[k]) < ITEM_TEXT_MIN_LEN:
                raise ValueError(
                    f"Text can't be shorter than {ITEM_TEXT_MIN_LEN} characters"
                )
            if len(info.data[k]) > ITEM_TEXT_MAX_LEN:
                raise ValueError(
                    f"Text can't be longer than {ITEM_TEXT_MAX_LEN} characters"
                )
        return v


class ItemCreate(ItemBase):
    pass


class ItemSchema(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_type: ItemTypes
    created_at: datetime
    status: ItemStatus


# response
class ItemOut(ItemSchema):
    pass
