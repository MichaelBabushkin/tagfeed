import enum

from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base
from .restriction_const import ITEM_TEXT_MAX_LEN
from .item_type_utils import image_extensions


class ItemTypes(enum.Enum):
    # Item types TEXT saved in the text column while evry other type is saved to the storage
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    NOT_DEFINED = "NOT_DEFINED"


class ItemStatus(enum.Enum):
    SAVING = "SAVING"
    CREATED = "CREATED"
    FAILED = "FAILED"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    item_type = Column(Enum(ItemTypes), nullable=False)
    item_text = Column(String(ITEM_TEXT_MAX_LEN), nullable=True)
    status = Column(
        Enum(ItemStatus), nullable=False, server_default=ItemStatus.CREATED.name
    )
    content_uuid = Column(UUID(as_uuid=True), nullable=True)
    preview_uuid = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    @staticmethod
    def filename_to_filetype(filename):
        ext = filename.rsplit(".", 1)[-1]
        if ext.upper() in image_extensions:
            return ItemTypes.IMAGE
        return ItemTypes.NOT_DEFINED
