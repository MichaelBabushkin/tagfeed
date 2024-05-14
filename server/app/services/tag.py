from typing import List

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from ..models.user import User
from ..models.tag import Tag
from ..schemas.tag import TagCreate
from ..database import get_session


class TagCreationFailed(Exception):
    pass


# Create tag
def create_new_tag(tag: TagCreate, user: User):
    new_tag = Tag(user_id=user.id, **tag.model_dump())
    with get_session() as session:
        session.add(new_tag)
        try:
            session.commit()
        except IntegrityError as e:
            if (
                isinstance(e.orig, UniqueViolation)
                and e.orig.diag.constraint_name == "name_user_id_uc"
            ):
                err_detail = f"user {user.username} has tag named {tag.name}"
                raise TagCreationFailed(err_detail)
            raise e
        session.refresh(new_tag)  # Used to add id to new_tag
    return new_tag


def create_tags(tags: List[TagCreate], user: User):
    with get_session() as session:
        db_tags = set(session.query(Tag).filter(Tag.user_id == user.id).all())
        db_tags_names = set([t.name for t in db_tags])
    not_existing_tags = list(filter(lambda tag: not tag.name in db_tags_names, tags))
    with get_session() as session:
        for new_tag in not_existing_tags:
            session.add(Tag(user_id=user.id, **new_tag.model_dump()))
        session.commit()
