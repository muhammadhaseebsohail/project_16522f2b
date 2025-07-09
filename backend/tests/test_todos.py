from fastapi.testclient import TestClient
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.authentication import JWTAuthentication
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import pytest
import app

@pytest.fixture
def test_client():
    return TestClient(app.app)

@pytest.fixture
def test_user():
    return {"username": "test", "password": "test"}

@pytest.fixture
def test_todo():
    return {"title": "Test Todo", "completed": False}

def test_create_todo_success(test_client, test_user, test_todo):
    response = test_client.post("/todos/", json=test_todo)
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_todo_fail_no_data(test_client, test_user):
    response = test_client.post("/todos/")
    assert response.status_code == 422

def test_read_todo_success(test_client, test_user, test_todo):
    post_response = test_client.post("/todos/", json=test_todo)
    todo_id = post_response.json()["id"]
    response = test_client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == test_todo

def test_read_todo_fail_invalid_id(test_client, test_user):
    response = test_client.get("/todos/invalid_id")
    assert response.status_code == 404

def test_update_todo_success(test_client, test_user, test_todo):
    post_response = test_client.post("/todos/", json=test_todo)
    todo_id = post_response.json()["id"]
    updated_todo = {"title": "Updated Todo", "completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=updated_todo)
    assert response.status_code == 200
    read_response = test_client.get(f"/todos/{todo_id}")
    assert read_response.json() == updated_todo

def test_update_todo_fail_invalid_id(test_client, test_user, test_todo):
    response = test_client.put("/todos/invalid_id", json=test_todo)
    assert response.status_code == 404

def test_delete_todo_success(test_client, test_user, test_todo):
    post_response = test_client.post("/todos/", json=test_todo)
    todo_id = post_response.json()["id"]
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    read_response = test_client.get(f"/todos/{todo_id}")
    assert read_response.status_code == 404

def test_delete_todo_fail_invalid_id(test_client, test_user):
    response = test_client.delete("/todos/invalid_id")
    assert response.status_code == 404

def test_authentication_required(test_client):
    response = test_client.get("/todos/")
    assert response.status_code == 401

def test_authentication_success(test_client, test_user):
    response = test_client.post("/auth/jwt/login", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()