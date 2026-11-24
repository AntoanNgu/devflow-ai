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

def test_me_with_valid_token(db_session):
    register_response = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert register_response.status_code == 201
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "stringisstring12"})
    assert login_response.status_code == 200
    data = login_response.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/auth/me", headers=headers)
    me_data = me_response.json()
    assert me_response.status_code == 200
    assert me_data["email"] == "test@example.com"
    assert "password_hash" not in me_data

def test_me_without_token(db_session):
    me_response = client.get("/auth/me")
    assert me_response.status_code == 401
    assert me_response.json()["detail"] == "Could not validate credentials"