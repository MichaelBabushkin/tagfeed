from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base


class UserTag(Base):
    __tablename__ = "users_tags"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
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
