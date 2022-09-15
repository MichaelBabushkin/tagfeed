import pytest

from app.schemas.tag import TagOut
from app.models.restriction_const import (
    TAG_NAME_MIN_LEN,
    TAG_NAME_MAX_LEN,
)
from app.oauth2 import verify_access_token
from .conftest import override_get_session
from app.models.user import User


def create_tag(authorized_client, test_user, name, status_code):
    res = authorized_client.post(
        "/tags/",
        json={
            "name": name,
        },
    )
    assert res.status_code == status_code
    if res.status_code == 201:
        new_tag = TagOut(**res.json())
        assert new_tag.name == name
        assert new_tag.user_id == test_user["id"]


@pytest.mark.parametrize(
    "name,                       status_code", [
    ("traveling",                201),
    ("r"*(TAG_NAME_MAX_LEN + 1), 422),
    ("r"*(TAG_NAME_MIN_LEN - 1), 422),
])
def test_create_tag(
    authorized_client, test_user, name, status_code
):
    create_tag(authorized_client, test_user, name, status_code)


def test_create_same_tag(authorized_client, test_user):
    def post_tag(tag_name):
        return authorized_client.post(
            "/tags/",
            json={
                "name": tag_name,
            },
        )

    tag_name = "tag1"
    res = post_tag(tag_name)
    assert res.status_code == 201
    new_tag = TagOut(**res.json())
    assert new_tag.name == tag_name
    assert new_tag.user_id == test_user["id"]
    res = post_tag(tag_name)
    assert res.status_code == 422


def test_create_tag_with_same_name(client, token, token2):
    tokens = [token, token2]
    name = "tagush"

    def send():
        return client.post(
            "/tags/",
            json={
                "name": name,
            },
        )

    for token in tokens:
        client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
        res = send()
        assert res.status_code == 201, "Could not create tag"
        new_tag = TagOut(**res.json())
        assert new_tag.name == name, "Tag's name isn't correct"
        token_data = verify_access_token(token)
        with override_get_session() as session:
            uid = (
                session.query(User)
                .filter(User.username == token_data.username)
                .first()
                .id
            )
        assert uid == new_tag.user_id, "Tag's user_id doesn't match"
