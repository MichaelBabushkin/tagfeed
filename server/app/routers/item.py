from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form, File
from typing_extensions import Annotated

from .. import oauth2
from ..models.user import User
from ..models.restriction_const import ITEM_TEXT_MAX_LEN
from ..schemas.item import ItemOut
from ..schemas.tag import TagCreate
from ..services.tag import not_existing_tags
from ..services.item import (
    get_items_list,
    get_an_item,
    create_new_item,
)

router = APIRouter(prefix="/items", tags=["items"])


# Get items
@router.get("/", response_model=List[ItemOut])
def get_items(
    current_user: User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    return get_items_list(limit, skip)


# Get item
@router.get("/{id}", response_model=ItemOut)
def get_item(id: int, current_user: User = Depends(oauth2.get_current_user)):
    item = get_an_item(id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id {id} doesn't exists",
        )
    return item


# Create item
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ItemOut)
def create_item(
    tags: Annotated[List[str], Form()] = [],
    text: Annotated[str, Form(max_length=ITEM_TEXT_MAX_LEN)] = None,
    file: Annotated[UploadFile, File] = None,
    current_user: User = Depends(oauth2.get_current_user),
):
    if file == None and (text in [None, ""]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error: An item must have text and/or file",
        )
    tags = list(
        filter(lambda tag: isinstance(tag, str) and tag.strip() != "", tags)
    )  # filter out non strings, strings which are spaces and empty strings
    if tags and len(tags) == 1:
        tags = [tag.strip() for tag in tags[0].split(",")]
    tags = [TagCreate(name=name) for name in tags]
    not_existing_tags_list = not_existing_tags(tags, current_user)
    if not_existing_tags_list:
        not_existing_tags_names = [t.name for t in not_existing_tags_list]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tags {not_existing_tags_names} don't exist",
        )
    return create_new_item(file, text, tags, current_user)
