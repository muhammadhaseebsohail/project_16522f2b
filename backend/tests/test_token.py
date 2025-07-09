from fastapi.testclient import TestClient
import pytest
from main import app, Todo, authenticate_user, get_current_user
from jose import JWTError, jwt

client = TestClient(app)

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

@pytest.fixture
def token():
    user = authenticate_user("admin", "admin")
    to_encode = user.copy()
    to_encode.update({"exp": 60})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

def test_read_todos(token):
    response = client.get("/todos", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 200

def test_read_todo_not_found(token):
    response = client.get("/todos/999", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 404

def test_create_todo(token):
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Description", "done": False},
                           headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 200
    assert response.json() == {"title": "Test Todo", "description": "Test Description", "done": False, "id": None}

def test_update_todo_not_found(token):
    response = client.put("/todos/999", json={"title": "Updated Todo", "description": "Updated Description", "done": True},
                          headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 404

def test_delete_todo_not_found(token):
    response = client.delete("/todos/999", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 404

def test_get_current_user_invalid_token():
    with pytest.raises(JWTError):
        get_current_user("Invalid Token")

def test_authenticate_user_invalid_credentials():
    with pytest.raises(Exception) as e:
        authenticate_user("wrong_username", "wrong_password")
    assert str(e.value) == "401 Unauthorized: Incorrect username or password"

def test_authenticate_user_valid_credentials():
    assert authenticate_user("admin", "admin") == {"username": "admin"}

def test_read_todos_limit_and_skip(token):
    response = client.get("/todos?skip=0&limit=1", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_read_todos_negative_skip(token):
    response = client.get("/todos?skip=-1&limit=1", headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 422

def test_create_todo_invalid_data(token):
    response = client.post("/todos", json={"title": "", "description": "Test Description", "done": False},
                           headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 422

def test_update_todo_invalid_data(token):
    response = client.put("/todos/999", json={"title": "", "description": "Updated Description", "done": True},
                          headers={"Authorization": f"Bearer {token['access_token']}"})
    assert response.status_code == 422

def test_login_unauthorized():
    response = client.post("/token", data={"username": "wrong_username", "password": "wrong_password"})
    assert response.status_code == 401

def test_login_authorized():
    response = client.post("/token", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"