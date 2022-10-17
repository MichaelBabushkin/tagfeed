import pytest

from .conftest import override_get_session
from app.schemas.item import ItemOut
from app.models.tag import Tag
from app.models.item import ItemTypes
from app.models.item_tag import ItemTag
from app.models.restriction_const import (
    ITEM_CONTENT_MIN_LEN,
    ITEM_CONTENT_MAX_LEN,
    ITEM_PREVIEW_MAX_LEN,
)


@pytest.mark.parametrize(
    "item_type,    content,                        preview,                        status_code", [
    ("STRING",      "r"*ITEM_CONTENT_MIN_LEN,       "r"*ITEM_PREVIEW_MAX_LEN,       201),
    ("LINK",        "r"*ITEM_CONTENT_MIN_LEN,       "r"*ITEM_PREVIEW_MAX_LEN,       201),
    ("NOT_DEFINED", "r"*ITEM_CONTENT_MIN_LEN,       "r"*ITEM_PREVIEW_MAX_LEN,       201),
    (1,             "r"*ITEM_CONTENT_MIN_LEN,       "r"*ITEM_PREVIEW_MAX_LEN,       422), # Bad item_type
    ("PIC",         "r"*ITEM_CONTENT_MIN_LEN,       "r"*ITEM_PREVIEW_MAX_LEN,       422), # Bad item_type
    ("STRING",      None,                           "r"*ITEM_PREVIEW_MAX_LEN,       422), # No content
    ("STRING",      "",                             "r"*ITEM_PREVIEW_MAX_LEN,       422), # Too short content
    ("STRING",      "r"*(ITEM_CONTENT_MIN_LEN - 1), "r"*ITEM_PREVIEW_MAX_LEN,       422), # Too short content
    ("STRING",      "r"*(ITEM_CONTENT_MAX_LEN + 1), "r"*ITEM_PREVIEW_MAX_LEN,       422), # Too long content
    ("STRING",      "r"*ITEM_CONTENT_MIN_LEN,       None,                           201), # No preview
    ("STRING",      "r"*ITEM_CONTENT_MIN_LEN,       "r"*(ITEM_PREVIEW_MAX_LEN + 1), 422), # Long preview
])
def test_create_item(test_user, authorized_client, item_type, content, preview, status_code):
    res = authorized_client.post(
        "/items/",
        json={"item": {"item_type": item_type, "content": content, "preview": preview}},
    )
    assert res.status_code == status_code
    if res.status_code == 201:
        new_item = ItemOut(**res.json())
        assert new_item.item_type == ItemTypes(item_type)
        assert new_item.content == content
        assert new_item.preview == preview
        with override_get_session() as session:
            tag = (
                session.query(Tag)
                .filter(
                    Tag.user_id == test_user["id"], Tag.name == test_user["username"]
                )
                .first()
            )
            item_tag = (
                session.query(ItemTag)
                .filter(ItemTag.item_id == new_item.id, ItemTag.tag_id == tag.id)
                .first()
            )
        assert (
            not item_tag is None
        ), "Item Creation didn't created an entry in the items_tags table"


def test_create_item_custom_tag(authorized_client, created_tag):
    res = authorized_client.post(
        "/items/",
        json={
            "item": {
                "item_type": "STRING",
                "content": "r" * ITEM_CONTENT_MIN_LEN,
                "preview": "r" * ITEM_PREVIEW_MAX_LEN,
            },
            "tags": [{"name": created_tag.name}],
        },
    )
    assert res.status_code == 201
    new_item = ItemOut(**res.json())
    assert new_item.item_type == ItemTypes("STRING")
    assert new_item.content == "r" * ITEM_CONTENT_MIN_LEN
    assert new_item.preview == "r" * ITEM_PREVIEW_MAX_LEN
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
        json={
            "item": {
                "item_type": "STRING",
                "content": "r" * ITEM_CONTENT_MIN_LEN,
                "preview": "r" * ITEM_PREVIEW_MAX_LEN,
            },
            "tags": [{"name": "random_tag_name"}],
        },
    )
    print(res.json())
    assert (
        res.status_code == 404
    ), "Should be an 404 error because tag random_tag_name doesn't exists"


def test_create_item_unauth(client):
    res = client.post(
        "/items/",
        json={
            "item": {
                "item_type": "STRING",
                "content": "r" * ITEM_CONTENT_MIN_LEN,
                "preview": "r" * ITEM_PREVIEW_MAX_LEN,
            }
        },
    )
    assert res.status_code == 401


def test_get_item_by_id(authorized_client, created_item):
    res = authorized_client.get(f"/items/{created_item.id}")
    assert res.status_code == 200, "Couldn't get item"
    item = ItemOut(**res.json())
    assert item.id == created_item.id
    assert item.content == created_item.content
    assert item.preview == created_item.preview


def test_get_item_by_id_unauth(client):
    res = client.get(f"/items/1")
    assert res.status_code == 401


def test_get_items(authorized_client, created_items):
    res = authorized_client.get("/items/")
    assert res.status_code == 200, "Couldn't get item"
    items_list = res.json()
    assert len(items_list) == len(created_items)
    for idx, item in enumerate(items_list):
        items_list[idx] = ItemOut(**item)
    created_items.sort(key=lambda x: x.id)
    items_list.sort(key=lambda x: x.id)
    for item, created_item in zip(items_list, created_items):
        assert item.id == created_item.id
        assert item.content == created_item.content
        assert item.preview == created_item.preview


def test_get_items_unauth(client):
    res = client.get(f"/items/")
    assert res.status_code == 401
