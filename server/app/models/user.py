from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import validates

from ..database import Base
from .restriction_const import (
    USER_EMAIL_MIN_LEN,
    USER_EMAIL_MAX_LEN,
    USER_PASSWORD_MIN_LEN,
    USER_PASSWORD_MAX_LEN,
    USER_USERNAME_MIN_LEN,
    USER_USERNAME_MAX_LEN,
    USER_FIRST_NAME_MIN_LEN,
    USER_FIRST_NAME_MAX_LEN,
    USER_LAST_NAME_MIN_LEN,
    USER_LAST_NAME_MAX_LEN,
)


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column("email", String(USER_EMAIL_MAX_LEN), nullable=False, unique=True)
    password = Column("password", String(USER_PASSWORD_MAX_LEN), nullable=False)
    username = Column(
        "username", String(USER_USERNAME_MAX_LEN), nullable=False, unique=True
    )
    first_name = Column("first_name", String(USER_FIRST_NAME_MAX_LEN), nullable=False)
    last_name = Column("last_name", String(USER_LAST_NAME_MAX_LEN), nullable=False)
    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    __table_args__ = (
        CheckConstraint(
            f"char_length(email) >= {USER_EMAIL_MIN_LEN}", name="email_min_length"
        ),
        CheckConstraint(
            f"char_length(username) >= {USER_USERNAME_MIN_LEN}",
            name="username_min_length",
        ),
        CheckConstraint(
            f"char_length(password) >= {USER_PASSWORD_MIN_LEN}",
            name="password_min_length",
        ),
        CheckConstraint(
            f"char_length(first_name) >= {USER_FIRST_NAME_MIN_LEN}",
            name="first_name_min_length",
        ),
        CheckConstraint(
            f"char_length(last_name) >= {USER_LAST_NAME_MIN_LEN}",
            name="last_name_min_length",
        ),
    )

    @validates("email")
    def validate_email_min_len(self, key, email) -> str:
        if len(email) <= USER_EMAIL_MIN_LEN:
            raise ValueError(
                f"email should be at least {USER_EMAIL_MIN_LEN} characters long"
            )
        return email

    @validates("username")
    def validate_username_min_len(self, key, username) -> str:
        if len(username) < USER_USERNAME_MIN_LEN:
            raise ValueError(
                f"username should be at least {USER_USERNAME_MIN_LEN} characters long"
            )
        return username

    @validates("password")
    def validate_password_min_len(self, key, password) -> str:
        if len(password) < USER_PASSWORD_MIN_LEN:
            raise ValueError(
                f"password should be at least {USER_PASSWORD_MIN_LEN} characters long"
            )
        return password

    @validates("first_name")
    def validate_first_name_min_len(self, key, first_name) -> str:
        if len(first_name) < USER_FIRST_NAME_MIN_LEN:
            raise ValueError(
                f"first_name should be at least {USER_FIRST_NAME_MIN_LEN} characters long"
            )
        return first_name

    @validates("last_name")
    def validate_last_name_min_len(self, key, last_name) -> str:
        if len(last_name) < USER_LAST_NAME_MIN_LEN:
            raise ValueError(
                f"last_name should be at least {USER_LAST_NAME_MIN_LEN} characters long"
            )
        return last_name
