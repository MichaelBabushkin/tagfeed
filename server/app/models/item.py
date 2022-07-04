import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import validates

from ..database import Base
from .restriction_const import (
    ITEM_CONTENT_MIN_LEN,
    ITEM_CONTENT_MAX_LEN,
    ITEM_PREVIEW_MAX_LEN,
)


class ItemTypes(enum.Enum):
    STRING = "STRING"
    LINK = "LINK"
    NOT_DEFINED = "NOT_DEFINED"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    item_type = Column(Enum(ItemTypes), nullable=False)
    content = Column(String(ITEM_CONTENT_MAX_LEN), nullable=False)
    preview = Column(String(ITEM_PREVIEW_MAX_LEN), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            f"char_length(content) >= {ITEM_CONTENT_MIN_LEN}", name="content_min_length"
        ),
    )

    @validates("content")
    def validate_content_min_len(self, key, content) -> str:
        if len(content) < ITEM_CONTENT_MIN_LEN:
            raise ValueError(
                f"content should be at least {ITEM_CONTENT_MIN_LEN} characters long"
            )
        return content
