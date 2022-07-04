from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..schemas.token import Token
from ..services.auth import login_user

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    token_dict = login_user(user_credentials)
    if token_dict is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentilas"
        )
    return token_dict
