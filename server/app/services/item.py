from typing import List

from sqlalchemy import desc

from ..models.tag import Tag
from ..models.item import Item
from ..models.user import User
from ..models.item_tag import ItemTag
from ..schemas.item import ItemCreate
from ..schemas.tag import TagCreate
from ..database import get_session

# Get items
def get_items_list(limit, skip):
    with get_session() as session:
        items = (
            session.query(Item)
            .order_by(desc(Item.created_at))
            .limit(limit)
            .offset(skip)
            .all()
        )
    return items


# Get item
def get_an_item(id):
    with get_session() as session:
        item = session.query(Item).filter(Item.id == id).first()
    return item


# Create item
def create_new_item(item: ItemCreate, tags: List[TagCreate], user: User):
    tags = [TagCreate(name=user.username)] if not tags else tags
    with get_session() as session:
        new_item = Item(user_id=user.id, **item.dict())
        session.add(new_item)
        session.flush()
        session.refresh(new_item)
        db_tags = set(session.query(Tag).filter(Tag.user_id == user.id).all())
        for tag in tags:
            tag_object = next(t for t in db_tags if t.name == tag.name)
            item_tag = ItemTag(item_id=new_item.id, tag_id=tag_object.id)
            session.add(item_tag)
        session.expunge(new_item)
        session.commit()
    return new_item
