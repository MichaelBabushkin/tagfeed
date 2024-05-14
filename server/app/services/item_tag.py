from typing import List

from ..models.tag import Tag
from ..models.user import User
from ..models.item_tag import ItemTag
from ..schemas.tag import TagCreate
from ..database import get_session


def create_item_items_tags(item_id: int, input_tags: List[TagCreate], user: User):
    tags = [TagCreate(name=user.username)] if not input_tags else input_tags
    with get_session() as session:
        db_tags = set(session.query(Tag).filter(Tag.user_id == user.id).all())
        db_tags_dict = {tag.name: tag for tag in db_tags}
        for tag in tags:
            tag_object = db_tags_dict[tag.name]
            item_tag = ItemTag(item_id=item_id, tag_id=tag_object.id)
            session.add(item_tag)
        session.commit()
