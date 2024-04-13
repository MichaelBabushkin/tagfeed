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
from app.schemas.item import ItemOut
from app.schemas.tag import TagOut
from app.oauth2 import create_access_token


@pytest.fixture
def session():
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
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


def create_user(client, user_data):
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    with override_get_session() as session:
        new_user["id"] = (
            session.query(User)
            .filter(User.username == user_data["username"])
            .first()
            .id
        )
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "username@ex.ex",
        "username": "username",
        "password": "password",
        "first_name": "Leonid",
        "last_name": "pantaler",
    }
    return create_user(client, user_data)


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "username1@ex.ex",
        "username": "username1",
        "password": "password",
        "first_name": "Leonid1",
        "last_name": "pantaler1",
    }
    return create_user(client, user_data)


@pytest.fixture
def token(test_user):
    return create_access_token({"username": test_user["username"]})


@pytest.fixture
def token2(test_user2):
    return create_access_token({"username": test_user2["username"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def created_item(authorized_client):
    res = authorized_client.post(
        "/items/",
        data={"text": "A test item"},
    )
    return ItemOut(**res.json())


@pytest.fixture
def created_items(authorized_client):
    item1 = authorized_client.post(
        "/items/",
        data={"text": "A test item"},
    )
    item2 = authorized_client.post(
        "/items/",
        data={"text": "A second test item"},
    )
    return [ItemOut(**item1.json()), ItemOut(**item2.json())]


@pytest.fixture
def created_tag(authorized_client):
    res = authorized_client.post(
        "/tags/",
        json={
            "name": "tagush",
        },
    )
    return TagOut(**res.json())
