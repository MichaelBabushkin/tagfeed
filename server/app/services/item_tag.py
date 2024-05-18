from typing import List

from sqlalchemy import func

from ..models.tag import Tag
from ..models.user import User
from ..models.item_tag import ItemTag
from ..schemas.tag import TagCreate
from ..database import get_session


def create_item_tags_for_item(item_id: int, input_tags: List[TagCreate], user: User):
    tags = [TagCreate(name=user.username)] if not input_tags else input_tags
    with get_session() as session:
        db_tags = set(session.query(Tag).filter(Tag.user_id == user.id).all())
        db_tags_dict = {tag.name: tag for tag in db_tags}
        for tag in tags:
            tag_object = db_tags_dict[tag.name]
            item_tag = ItemTag(item_id=item_id, tag_id=tag_object.id)
            session.add(item_tag)
        session.commit()


def delete_item_tags_for_item(item_id: int):
    with get_session() as session:
        subquery = (
            session.query(ItemTag.tag_id).filter(ItemTag.item_id == item_id).subquery()
        )
        count_query = (
            session.query(ItemTag.tag_id, func.count(ItemTag.tag_id).label("count"))
            .filter(ItemTag.tag_id.in_(subquery))
            .group_by(ItemTag.tag_id)
            .all()
        )
    tag_ids = [(row[0], row[1]) for row in count_query]
    tag_ids_to_delete = list(
        map(lambda row: row[0], filter(lambda row: row[1] == 1, tag_ids))
    )
    with get_session() as session:
        session.query(ItemTag).filter(ItemTag.item_id == item_id).delete()
        session.commit()
    return tag_ids_to_delete
