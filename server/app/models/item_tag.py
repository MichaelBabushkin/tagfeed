from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base


class ItemTag(Base):
    __tablename__ = "items_tags"
    item_id = Column(
        Integer,
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    tag_id = Column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    created_at = Column(
        TIMESTAMP(timezone=False), nullable=False, server_default=text("now()")
    )
