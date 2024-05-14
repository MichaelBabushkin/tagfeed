import pytest
from jose import jwt

from app.config import settings
from app.schemas.token import Token


@pytest.mark.parametrize(
    "username, password",
    [
        ("username", "password"), # login by username
        ("username@ex.ex", "password"),  # login by email
    ],
)
def test_login_user(test_user, client, username, password):
    res = client.post(
        "/login",
        data={"username": username, "password": password},
    )
    assert res.status_code == 200
    login_res = Token(**res.json())
    assert login_res.token_type == "bearer"
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    payload_username = payload.get("username")
    assert payload_username == test_user["username"], "Couldn't login"


@pytest.mark.parametrize(
    "username,        password,         status_code",
    [
        ("wrong_username", "wrong_password", 403),  # wrong username and password
        ("wrong_username", "password", 403),  # wrong username
        ("username", "wrong_password", 403),  # wrong password
        (None, "password", 422),  # no username
        ("username", None, 422),  # no password
        (None, None, 422),  # no username and password
    ],
)
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == status_code
