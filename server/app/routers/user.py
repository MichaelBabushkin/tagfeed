from fastapi import APIRouter, status, HTTPException
from pydantic import EmailStr, constr

from ..schemas.user import UserCreate, UserOut
from ..services.user import email_exists, username_exists, create_user, get_user_by_id
from app.models.restriction_const import USER_USERNAME_MIN_LEN, USER_USERNAME_MAX_LEN

router = APIRouter(prefix="/users", tags=["users"])

# Check free email while creating
@router.get("/email_exists", status_code=status.HTTP_404_NOT_FOUND)
@router.get("/email_exists/{email}", status_code=status.HTTP_200_OK)
def check_email_exists(email: EmailStr):
    return email_exists(email)


# Check free username while creating
@router.get("/username_exists", status_code=status.HTTP_404_NOT_FOUND)
@router.get("/username_exists/{username}", status_code=status.HTTP_200_OK)
def check_username_exists(
    username: constr(
        regex=r"[a-zA-Z0-9]+",
        min_length=USER_USERNAME_MIN_LEN,
        max_length=USER_USERNAME_MAX_LEN,
    )
):
    return username_exists(username)


# Create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_new_user(user: UserCreate):
    if username_exists(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with with username {user.username} already exists",
        )
    if email_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with with email {user.email} already exists",
        )
    try:
        new_user = create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int):
    user = get_user_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} doesn't exists",
        )
    return user
