import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions

# This part is to use a separate db for the test environment
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    return TestingSessionLocal()


import app.database as database

database.get_session = override_get_session

from app.main import app
from app.database import Base
from app.models.user import User
from app.models.tag import Tag
from app.models.item import Item
from app.models.user_tag import UserTag
from app.models.item_tag import ItemTag
from app.models.restriction_const import ITEM_CONTENT_MIN_LEN, ITEM_PREVIEW_MAX_LEN
from app.schemas.item import ItemOut
from app.oauth2 import create_access_token


@pytest.fixture
def session():
    db = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        close_all_sessions()
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture
def client(session):
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "username@ex.ex",
        "username": "username",
        "password": "password",
        "first_name": "Leonid",
        "last_name": "pantaler",
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"username": test_user["username"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def created_item(authorized_client):
    res = authorized_client.post(
        "/items/",
        json={
            "item_type": "STRING",
            "content": "r" * ITEM_CONTENT_MIN_LEN,
            "preview": "r" * ITEM_PREVIEW_MAX_LEN,
        },
    )
    return ItemOut(**res.json())


@pytest.fixture
def created_items(authorized_client):
    item1 = authorized_client.post(
        "/items/",
        json={
            "item_type": "STRING",
            "content": "r" * ITEM_CONTENT_MIN_LEN,
            "preview": "r" * ITEM_PREVIEW_MAX_LEN,
        },
    )
    item2 = authorized_client.post(
        "/items/",
        json={
            "item_type": "LINK",
            "content": "L" * ITEM_CONTENT_MIN_LEN,
            "preview": "L" * ITEM_PREVIEW_MAX_LEN,
        },
    )
    return [ItemOut(**item1.json()), ItemOut(**item2.json())]
