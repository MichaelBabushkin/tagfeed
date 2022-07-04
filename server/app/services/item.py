from sqlalchemy import desc

from ..models.item import Item
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
def create_new_item(item, current_user):
    new_item = Item(user_id=current_user.id, **item.dict())
    with get_session() as session:
        session.add(new_item)
        session.commit()
        session.refresh(new_item)  # Used to add id and created_at to new_item
    return new_item
