import uuid
from typing import List

from fastapi import File
from sqlalchemy import desc

from ..models.tag import Tag
from ..models.item import Item, ItemStatus, ItemTypes
from ..models.user import User
from ..models.item_tag import ItemTag
from ..schemas.tag import TagCreate
from ..database import get_session
from ..storage_handler_utils import upload_item, download_item


class ContentCreationFailed(Exception):
    pass


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
        if item and item.content_uuid and item.status != ItemStatus.FAILED:
            res = download_item(str(item.content_uuid))
            if res.error:
                print(res.error)
                return None
            item.content = res.content
    return item


# Create item
def create_new_item(file: File, item_text: str, tags: List[TagCreate], user: User):
    tags = [TagCreate(name=user.username)] if not tags else tags
    item_type = (
        ItemTypes.TEXT if file is None else Item.filename_to_filetype(file.filename)
    )
    content_uuid = None if item_type == ItemTypes.TEXT else uuid.uuid4()
    status = ItemStatus.CREATED if item_type == ItemTypes.TEXT else ItemStatus.SAVING
    with get_session() as session:
        new_item = Item(
            user_id=user.id,
            item_type=item_type,
            item_text=item_text,
            content_uuid=content_uuid,
            status=status,
        )
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
    if status != ItemStatus.SAVING:
        return new_item
    data = file.file.read()
    try:  # might fail because the service is down or due to internal error of the service
        upload_result = upload_item(str(content_uuid), data)
    except Exception as e:
        upload_result = e
        upload_result.status = str(e)
    if upload_result.status != "ok":
        with get_session() as session:
            queried_item = session.query(Item).filter_by(id=new_item.id).first()
            queried_item.status = ItemStatus.FAILED
            queried_item.content_uuid = None
            session.query(ItemTag).filter(ItemTag.item_id == new_item.id).delete()
            session.flush()
            session.refresh(queried_item)
            session.expunge(queried_item)
            session.commit()
        return queried_item
    with get_session() as session:
        queried_item = session.query(Item).filter_by(id=new_item.id).first()
        queried_item.status = ItemStatus.CREATED
        session.flush()
        session.refresh(queried_item)
        session.expunge(queried_item)
        session.commit()
    return queried_item
