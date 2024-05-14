from .. import crypto_utils, oauth2
from ..models.user import User
from ..database import get_session


def login_user(user_credentials):
    with get_session() as session:
        if '@' in user_credentials.username:
            condition = User.email == user_credentials.username
        else:
            condition = User.username == user_credentials.username
        user = (
            session.query(User)
            .filter(condition)
            .first()
        )
    if not user:
        return
    if not crypto_utils.verify(user_credentials.password, user.password):
        return
    access_token = oauth2.create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
