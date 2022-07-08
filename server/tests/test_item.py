import pytest

from .conftest import override_get_session
from app.schemas.item import ItemOut
from app.models.tag import Tag
from app.models.item import ItemTypes, ItemStatus
from app.models.item_tag import ItemTag
from app.models.restriction_const import (
    ITEM_TEXT_MAX_LEN,
    ITEM_TEXT_MIN_LEN,
)


@pytest.mark.parametrize(
    "item_text,                   tags,                status_code", [
    ("r"*ITEM_TEXT_MAX_LEN,       None,               201),
    ("r"*ITEM_TEXT_MIN_LEN,       None,               201),
    ("r"*ITEM_TEXT_MAX_LEN,       ["tag1"],           404), # Tag doesn't exist
    ("r"*ITEM_TEXT_MAX_LEN,       ["tag1", "tag2"],   404), # Tags don't exist
    ("r"*0,                       None,               400), # Nothing
    ("r"*(ITEM_TEXT_MIN_LEN - 1), None,               400), # Nothing
    ("r"*(ITEM_TEXT_MAX_LEN + 1), None,               422), # Too long content
])
def test_create_text_item(test_user, authorized_client, item_text, tags, status_code):
    data = dict()
    if item_text:
        data['text'] = item_text
    if tags:
        data['tags'] = tags
    res = authorized_client.post(
        "/items/",
        data=data,
    )
    assert res.status_code == status_code
    if res.status_code == 201:
        new_item = ItemOut(**res.json())
        assert new_item.item_type == ItemTypes.TEXT
        assert new_item.item_text == item_text
        with override_get_session() as session:
            if tags is None:
                tags = [test_user["username"]]
            _tags = (
                session.query(Tag)
                .filter(
                    Tag.user_id == test_user["id"]
                )
                .all()
            )
            _tags_names = [tag.name for tag in _tags]
            assert set(tags).intersection(set(_tags_names)) == set(tags), "Not all tags were created"
            _tags = list(filter(lambda tag: tag.name in tags, _tags))
            for tag in _tags:
                item_tag = (
                    session.query(ItemTag)
                    .filter(ItemTag.item_id == new_item.id, ItemTag.tag_id == tag.id)
                    .first()
                )
                assert (
                    not item_tag is None
                ), f"Item Creation didn't created an entry {tag} in the items_tags table"


class UploadResp:
    def __init__(self, status):
        self.status = status


@pytest.mark.parametrize(
    "item_text,                tags, file_path,                    status_code",[
    ("Describtion for item 1", None, "./server/tests/tagfeed.png", 201),
])
def test_create_item_to_the_storage(test_user, authorized_client, mocker, item_text, tags, file_path, status_code):
    data = dict()
    file_content = None
    if file_path:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    if item_text:
        data['text'] = item_text
    if tags:
        data['tags'] = tags
    res = authorized_client.post(
        "/items/",
        data=data,
    )
    if file_content:
        res = authorized_client.post(
            "/items/",
            data=data,
            files={'file': file_content}
        )
    else:
        res = authorized_client.post(
            "/items/",
            data=data
        ) 
    assert res.status_code == status_code
    new_item = ItemOut(**res.json())
    assert new_item.status == ItemStatus("CREATED")
    assert new_item.item_text == item_text 


def test_create_item_custom_tag(authorized_client, created_tag):
    res = authorized_client.post(
        "/items/",
        data={
            "text": "Hey hey",
            "tags": [created_tag.name]
        }
    )
    assert res.status_code == 201
    new_item = ItemOut(**res.json())
    assert new_item.item_type == ItemTypes("TEXT")
    assert new_item.item_text == "Hey hey"
    with override_get_session() as session:
        item_tag = (
            session.query(ItemTag)
            .filter(ItemTag.item_id == new_item.id, ItemTag.tag_id == created_tag.id)
            .first()
        )
    assert (
        not item_tag is None
    ), "Item Creation didn't created an entry in the items_tags table"


def test_create_item_non_existing_custom_tag(authorized_client):
    res = authorized_client.post(
        "/items/",
        data={
            "text": "Hey hey",
            "tags": ["random_tag_name"]
        },
    )
    assert (
        res.status_code == 404
    ), "Should be an 404 error because tag random_tag_name doesn't exists"


def test_create_item_unauth(client):
    res = client.post(
        "/items/",
        data={
            "text": "Hey hey"
        },
    )
    assert res.status_code == 401


def test_get_item_by_id(authorized_client, created_item):
    res = authorized_client.get(f"/items/{created_item.id}")
    assert res.status_code == 200, "Couldn't get item"
    item = ItemOut(**res.json())
    assert item.id == created_item.id, "Item id isn't matching"
    assert item.item_text == created_item.item_text, "Item text isn't matching"
    assert item.item_type == ItemTypes("TEXT"), "Item type isn't matching"


def test_get_item_by_id_unauth(client):
    res = client.get(f"/items/1")
    assert res.status_code == 401


def test_get_items(authorized_client, created_items):
    res = authorized_client.get("/items/")
    assert res.status_code == 200, "Couldn't get item"
    items_list = res.json()
    assert len(items_list) == len(created_items), "number of items doesn't match"
    created_items.sort(key=lambda x: x.id)
    items_list.sort(key=lambda x: x['id'])
    for item, created_item in zip(items_list, created_items):
        assert item['id'] == created_item.id
        assert item['item_text'] == created_item.item_text
        assert item['item_type'] == "TEXT"


def test_get_items_unauth(client):
    res = client.get(f"/items/")
    assert res.status_code == 401
