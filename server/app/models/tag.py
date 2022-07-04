from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import validates

from ..database import Base
from .restriction_const import TAG_NAME_MIN_LEN, TAG_NAME_MAX_LEN


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(TAG_NAME_MAX_LEN), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            f"char_length(name) >= {TAG_NAME_MIN_LEN}", name="name_min_length"
        ),
    )

    @validates("name")
    def validate_name_min_len(self, key, name) -> str:
        if len(name) < TAG_NAME_MIN_LEN:
            raise ValueError(
                f"name should be at least {TAG_NAME_MIN_LEN} characters long"
            )
        return name
