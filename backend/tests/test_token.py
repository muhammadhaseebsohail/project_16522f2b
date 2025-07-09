import pytest
from fastapi.testclient import TestClient
from main import app, fake_users_db, authenticate_user, get_user, Deployment
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

client = TestClient(app)

def test_read_deployment():
    response = client.get("/deployments/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_token():
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}

def test_get_token_with_correct_credentials():
    response = client.post("/token", data={"username": "testuser", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.fixture
def token():
    response = client.post("/token", data={"username": "testuser", "password": "secret"})
    return response.json()["access_token"]

def test_read_deployment_with_token(token):
    response = client.get("/deployments/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Deployment", "version": "v1.0"}

def test_authenticate_user():
    user = authenticate_user(fake_users_db, "testuser", "secret")
    assert user.username == "testuser"
    assert user.disabled == False

def test_get_user():
    user = get_user(fake_users_db, "testuser")
    assert user.username == "testuser"
    assert user.disabled == False

def test_get_non_existing_user():
    user = get_user(fake_users_db, "nonexisting")
    assert user is None

def test_read_deployment_non_existing_id(token):
    response = client.get("/deployments/100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}

def test_deployment_model():
    deployment = Deployment(id=1, name="Test Deployment", version="v1.0")
    assert deployment.id == 1
    assert deployment.name == "Test Deployment"
    assert deployment.version == "v1.0"