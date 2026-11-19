from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_successful_register(db_session):
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] is not None
    assert "password_hash" not in data 

def test_register_duplicate_email(db_session):
    first = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert first.status_code == 201 
    second = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert second.status_code == 409
    assert second.json()["detail"] == "Email already registered"

def test_register_invalid_email(db_session):
    response = client.post("/auth/register", json={"email": "invalid-email", "password": "stringisstring12"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]

def test_login_success(db_session):
    register_response = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert register_response.status_code == 201
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "stringisstring12"})
    assert login_response.status_code == 200
    data = login_response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data

def test_wrong_password(db_session):
    register_response = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert register_response.status_code == 201
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "stringisnotstring12"})
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect email or password"

def test_unknown_email(db_session):
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "stringisnotstring12"})
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect email or password"

