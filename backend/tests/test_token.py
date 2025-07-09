import pytest
from fastapi.testclient import TestClient
from main import app, authenticate_user, fake_users_db, create_access_token, get_user
from datetime import timedelta

client = TestClient(app)

def test_get_user_success():
    user = get_user(fake_users_db, "alice")
    assert user.username == "alice"
    assert user.hashed_password == "fakehashedpassword"
    assert user.disabled == False

def test_get_user_fail():
    user = get_user(fake_users_db, "bob")
    assert user == None

def test_authenticate_user_success():
    user = authenticate_user(fake_users_db, "alice", "fakehashedpassword")
    assert user.username == "alice"

def test_authenticate_user_fail():
    user = authenticate_user(fake_users_db, "bob", "wrongpassword")
    assert user == False

def test_create_access_token():
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": "alice"}, expires_delta=access_token_expires
    )
    assert isinstance(access_token, str)

def test_login_for_access_token_success():
    response = client.post(
        "/token",
        data={
            "username": "alice",
            "password": "fakehashedpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_fail():
    response = client.post(
        "/token",
        data={
            "username": "bob",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401

def test_read_users_me_success():
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": "alice"}, expires_delta=access_token_expires
    )
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_read_users_me_fail():
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer wrongtoken"},
    )
    assert response.status_code == 401