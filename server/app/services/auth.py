from .. import crypto_utils, oauth2
from ..models.user import User
from ..database import get_session


def login_user(user_credentials):
    with get_session() as session:
        user = (
            session.query(User)
            .filter(User.username == user_credentials.username)
            .first()
        )
    if not user:
        return
    if not crypto_utils.verify(user_credentials.password, user.password):
        return
    access_token = oauth2.create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
