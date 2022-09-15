from fastapi import APIRouter, Depends, status, HTTPException

from .. import oauth2
from ..models.user import User
from ..schemas.tag import TagOut, TagCreate
from ..services.tag import create_new_tag, TagCreationFailed

router = APIRouter(prefix="/tags", tags=["tags"])

# Create tag
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TagOut)
def create_tag(tag: TagCreate, current_user: User = Depends(oauth2.get_current_user)):
    try:
        return create_new_tag(tag, current_user)
    except TagCreationFailed as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
