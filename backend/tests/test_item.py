from fastapi.testclient import TestClient
from main import app, Item, verify_credentials
from fastapi.security import HTTPBasicCredentials
import pytest

client = TestClient(app)

@pytest.fixture
def valid_credentials():
    return HTTPBasicCredentials(username="admin", password="password")

@pytest.fixture
def invalid_credentials():
    return HTTPBasicCredentials(username="wrong", password="wrong")

@pytest.fixture
def valid_item():
    return {"name": "Test Item", "price": 50.0}

@pytest.fixture
def invalid_item():
    return {"name": "", "price": -10.0}

def test_create_item_success(valid_credentials, valid_item):
    response = client.post("/item/", auth=(valid_credentials.username, valid_credentials.password), json=valid_item)
    assert response.status_code == 200
    assert response.json() == valid_item

def test_create_item_fail_invalid_data(invalid_credentials, invalid_item):
    response = client.post("/item/", auth=(invalid_credentials.username, invalid_credentials.password), json=invalid_item)
    assert response.status_code == 422

def test_create_item_fail_unauthorized(valid_item):
    response = client.post("/item/", json=valid_item)
    assert response.status_code == 401

def test_read_item_success(valid_credentials):
    response = client.get("/item/1", auth=(valid_credentials.username, valid_credentials.password))
    assert response.status_code == 200
    assert response.json() == {"name": "item1", "price": 100.0}

def test_read_item_fail_unauthorized():
    response = client.get("/item/1")
    assert response.status_code == 401

def test_update_item_success(valid_credentials, valid_item):
    response = client.put("/item/1", auth=(valid_credentials.username, valid_credentials.password), json=valid_item)
    assert response.status_code == 200
    assert response.json() == {"name": "item1", "price": 50.0}

def test_update_item_fail_invalid_data(invalid_credentials, invalid_item):
    response = client.put("/item/1", auth=(invalid_credentials.username, invalid_credentials.password), json=invalid_item)
    assert response.status_code == 422

def test_update_item_fail_unauthorized(valid_item):
    response = client.put("/item/1", json=valid_item)
    assert response.status_code == 401

def test_delete_item_success(valid_credentials):
    response = client.delete("/item/1", auth=(valid_credentials.username, valid_credentials.password))
    assert response.status_code == 200
    assert response.json() == {"message": "Item successfully deleted"}

def test_delete_item_fail_unauthorized():
    response = client.delete("/item/1")
    assert response.status_code == 401

def test_verify_credentials_success(valid_credentials):
    assert verify_credentials(valid_credentials) == valid_credentials

def test_verify_credentials_fail(invalid_credentials):
    with pytest.raises(HTTPException):
        verify_credentials(invalid_credentials)