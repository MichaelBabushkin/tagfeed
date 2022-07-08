import datetime
from time import sleep
from multiprocessing import Process

from ..database import get_session
from ..models.item import Item, ItemStatus
from ..config import settings

minutes_threshohld = datetime.timedelta(minutes=settings.content_pending_expire_minutes)


def clean(threshohld):
    with get_session() as session:
        # items = session.query(Item).filter(Item.status == ItemStatus.CONTENT_PENDING, now() - Item.created_at >  ).all()
        items = (
            session.query(Item).filter(Item.status == ItemStatus.CONTENT_PENDING).all()
        )
        if items:
            now = datetime.datetime.now(datetime.UTC)
            items_to_delete = list(
                filter(
                    lambda item: now
                    - item.created_at.replace(tzinfo=None)
                    + item.created_at.tzinfo.utcoffset(item.created_at)
                    > threshohld,
                    items,
                )
            )
            ids_to_delete = list(map(lambda item: item.id, items_to_delete))
            session.query(Item).filter(Item.id.in_(ids_to_delete)).delete()
            session.commit()

if __name__ == "__main__":
    clean(minutes_threshohld)
