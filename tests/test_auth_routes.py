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
