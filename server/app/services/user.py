from ..models.user import User
from .. import utils
from ..database import get_session


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
        session.commit()
    return new_user


def get_user_by_id(id):
    with get_session() as session:
        user = session.query(User).filter(User.id == id).first()
    return user
