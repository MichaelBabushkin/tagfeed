from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from .. import oauth2
from ..models.user import User
from ..schemas.item import ItemOut, ItemCreate
from ..services.item import get_items_list, get_an_item, create_new_item

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
    item: ItemCreate, current_user: User = Depends(oauth2.get_current_user)
):
    return create_new_item(item, current_user)
