import pytest

from .conftest import override_get_session
from app.models.user import User
from app.models.tag import Tag
from app.schemas.user import UserOut
from app.models.restriction_const import (
    USER_PASSWORD_MIN_LEN,
    USER_PASSWORD_MAX_LEN,
    USER_USERNAME_MIN_LEN,
    USER_USERNAME_MAX_LEN,
    USER_FIRST_NAME_MIN_LEN,
    USER_FIRST_NAME_MAX_LEN,
    USER_LAST_NAME_MIN_LEN,
    USER_LAST_NAME_MAX_LEN,
)


@pytest.mark.parametrize(
    "email,            username,   password, first_name, last_name,  status_code",
    [
        ("mail@mail.com", "emaily", "12345", "Leonid", "pantaler", 201),
        ("mail1@mail.com", "emaily1", "12345", "Leonid", "pantaler", 201),
    ],
)
def test_create_user(
    client, email, username, password, first_name, last_name, status_code
):
    res = client.post(
        "/users/",
        json={
            "email": email,
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert res.status_code == status_code
    new_user = UserOut(**res.json())
    assert new_user.email == email
    assert new_user.username == username
    assert new_user.first_name == first_name
    assert new_user.last_name == last_name
    with override_get_session() as session:
        user_id = session.query(User).filter(User.username == username).first().id
        tag = session.query(Tag).filter(Tag.user_id == user_id).first().name
    assert tag == username, "Tag wasn't created"


@pytest.mark.parametrize(
    "email,             username,                         password,                         first_name,                        last_name,                        status_code",
    [
        ("username@ex.ex", "random", "random", "random", "random", 422),  # email exists
        ("username.ex.ex", "random", "random", "random", "random", 422),  # bad email
        (None, "random", "random", "random", "random", 422),  # no email
        ("a@a", "random", "random", "random", "random", 422),  # short email
        (
            "a@" + "ab" * 32 + ".c",
            "random",
            "random",
            "random",
            "random",
            422,
        ),  # long email
        (
            "username2@ex.ex",
            "username",
            "random",
            "random",
            "random",
            422,
        ),  # username exists
        ("random", None, "random", "random", "random", 422),  # no username
        (
            "random",
            "r" * (USER_USERNAME_MIN_LEN - 1),
            "random",
            "random",
            "random",
            422,
        ),  # short username
        (
            "random",
            "r" * (USER_USERNAME_MAX_LEN + 1),
            "random",
            "random",
            "random",
            422,
        ),  # long username
        ("username2@ex.ex", "random", None, "random", "random", 422),  # no password
        (
            "username2@ex.ex",
            "random",
            "r" * (USER_PASSWORD_MIN_LEN - 1),
            "random",
            "random",
            422,
        ),  # short password
        (
            "username2@ex.ex",
            "random",
            "r" * (USER_PASSWORD_MAX_LEN + 1),
            "random",
            "random",
            422,
        ),  # long password
        ("username2@ex.ex", "random", "random", None, "random", 422),  # no first_name
        (
            "username2@ex.ex",
            "random",
            "random",
            "r" * (USER_FIRST_NAME_MIN_LEN - 1),
            "random",
            422,
        ),  # short first_name
        (
            "username2@ex.ex",
            "random",
            "random",
            "r" * (USER_FIRST_NAME_MAX_LEN + 1),
            "random",
            422,
        ),  # long first_name
        ("username2@ex.ex", "random", "random", "random", None, 422),  # no last_name
        (
            "username2@ex.ex",
            "random",
            "random",
            "random",
            "r" * (USER_LAST_NAME_MIN_LEN - 1),
            422,
        ),  # short last_name
        (
            "username2@ex.ex",
            "random",
            "random",
            "random",
            "r" * (USER_LAST_NAME_MAX_LEN + 1),
            422,
        ),  # long last_name
    ],
)
def test_incorrect_create_user(
    client, test_user, email, username, password, first_name, last_name, status_code
):
    res = client.post(
        "/users/",
        json={
            "email": email,
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert res.status_code == status_code


def test_get_user_by_id(test_user, client):
    res = client.get(f"/users/1")
    user_data = res.json()
    assert test_user["email"] == user_data["email"], "User email doesn't match"
    assert test_user["username"] == user_data["username"], "User username doesn't match"
    assert (
        test_user["first_name"] == user_data["first_name"]
    ), "User first_name doesn't match"
    assert (
        test_user["last_name"] == user_data["last_name"]
    ), "User last_name doesn't match"


@pytest.mark.parametrize(
    "id,      status_code",
    [
        ("2", 404),  # user doesn't exist
        ("-1", 404),  # user doesn't exist
        ("-2", 404),  # user doesn't exist
        ("770", 404),  # user doesn't exist
        ("770.1", 422),  # bad user id
        ("-2.5", 422),  # bad user id
        ("abc", 422),  # bad user id
    ],
)
def test_incorrect_get_user_by_id(client, id, status_code):
    res = client.get(f"/users/{id}")
    assert (
        res.status_code == status_code
    ), f"status_code is {res.status_code} but we were expecting {status_code}"


@pytest.mark.parametrize(
    "email,            status_code",
    [
        ("username@ex.ex", 200),  # email exists
        ("usernamxe@x.ex", 200),  # email doesn't exist
        ("a@a.a", 200),  # email doesn't exist
        (None, 422),  # email isn't valid
        (1234567, 422),  # email isn't valid
        ("a@a", 422),  # email isn't valid
    ],
)
def test_email_exists(test_user, client, email, status_code):
    res = client.get(f"/users/email_exists/{email}")
    assert (
        res.status_code == status_code
    ), f"status_code is {res.status_code} but we were expecting {status_code}"


@pytest.mark.parametrize(
    "username,   status_code",
    [
        ("username", 200),  # username exists
        ("urrrnnne", 200),  # username doesn't exist
        (1234567, 200),  # username doesn't exist
        (None, 422),  # username isn't valid
        ("a@a", 422),  # username isn't valid
    ],
)
def test_username_exists(test_user, client, username, status_code):
    res = client.get(f"/users/username_exists/{username}")
    assert (
        res.status_code == status_code
    ), f"status_code is {res.status_code} but we were expecting {status_code}"
