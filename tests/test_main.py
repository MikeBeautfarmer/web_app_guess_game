import os
import pytest
from main import app, db
from models import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()

    db.create_all()

    yield client


@pytest.fixture
def user():
    user = User(
        name="John",
        email="john.do@something.com",
        session_token="token"
    )
    db.add(user)
    db.commit()

    return user


@pytest.fixture
def client_authenticated(client, user):
    client.set_cookie("localhost", "session_token", user.session_token)

    return client


def cleanup():
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get("/")
    assert b"Dein Name" in response.data


def test_placeholder_login(client):
    response = client.get("/")
    assert b"Dein Name" in response.data


def test_index_logged_in(client):
    response = client.get("/game")
    assert b"Gib mir eine Zahl" in response.data


def test_logged_in_index(client):
    client.set_cookie("localhost", "session_token", "token")
    response = client.get("/", follow_redirects=True)
    assert b"Dein Name" in response.data


def test_login(client):
    response = client.post(
        "/login",
        data={"user-name": "Test user", "user-email": "test@test.com", "user-password": "password123"})
    assert response.headers["Location"] == "http://localhost/"

    response = client.get("/game")
    assert b"Gib mir eine Zahl" in response.data


def test_profile(client, user):
    client.set_cookie("localhost", "session_token", "token")
    response = client.get("/profile")
    assert b"john.do@something.com" in response.data


def test_logged_in_index2(client_authenticated):
    response = client_authenticated.get("/game")
    assert b"Gib mir eine Zahl" in response.data


def test_profile2(client_authenticated):
    response = client_authenticated.get("/profile")
    assert b"John" in response.data
