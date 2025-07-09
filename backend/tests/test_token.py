from fastapi.testclient import TestClient
from fastapi import status
import pytest
from main import app, authenticate_user, fake_users_db

client = TestClient(app)

def test_login_for_access_token_success():
    response = client.post("/token", data={"username": "johndoe", "password": "password"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_login_for_access_token_invalid_username():
    response = client.post("/token", data={"username": "invalidusername", "password": "password"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_for_access_token_invalid_password():
    response = client.post("/token", data={"username": "johndoe", "password": "invalidpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_for_access_token_empty_username():
    response = client.post("/token", data={"username": "", "password": "password"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_login_for_access_token_empty_password():
    response = client.post("/token", data={"username": "johndoe", "password": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_login_for_access_token_no_data():
    response = client.post("/token", data={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_authenticate_user_success():
    assert authenticate_user(fake_users_db, "johndoe", "password")

def test_authenticate_user_invalid_username():
    assert not authenticate_user(fake_users_db, "invalidusername", "password")

def test_authenticate_user_invalid_password():
    assert not authenticate_user(fake_users_db, "johndoe", "invalidpassword")