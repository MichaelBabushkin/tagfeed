import datetime
from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import database
from .schemas.token import TokenData
from .models.user import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenVerificationError(Exception):
    pass


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise TokenVerificationError
        token_data = TokenData(username=username)
    except JWTError:
        raise TokenVerificationError
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(database.get_session),
):
    excep = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = verify_access_token(token)
    except TokenVerificationError:
        raise excep
    with session:
        user = session.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise excep
    return user
