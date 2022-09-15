from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from .tag import create_new_tag, TagCreationFailed
from ..models.user import User
from ..schemas.tag import TagCreate
from .. import utils
from ..database import get_session


class UserCreationFailed(Exception):
    pass


def email_exists(email):
    with get_session() as session:
        query_result = session.query(User).filter(User.email == email).first()
    if query_result is None:
        return False
    return True


def username_exists(username):
    with get_session() as session:
        query_result = session.query(User).filter(User.username == username).first()
    if query_result is None:
        return False
    return True


def create_user(user):
    user.password = utils.hash(user.password)
    new_user = User(**user.dict())
    with get_session() as session:
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                key = e.orig.diag.constraint_name.split("_")[1]
                err_detail = (
                    f"{key} must be unique. {getattr(user, key)} already exists."
                )
                raise UserCreationFailed(err_detail)
            raise e
        session.refresh(new_user)
    try:
        create_new_tag(TagCreate(name=user.username), new_user)
    except TagCreationFailed as e:
        err_detail = (
            f"somethinng went wrong couldn't create user's default tag\nerror:{e}"
        )
        raise UserCreationFailed(err_detail)
    return user


def get_user_by_id(id):
    with get_session() as session:
        user = session.query(User).filter(User.id == id).first()
    return user
