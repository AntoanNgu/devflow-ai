import os
from dotenv import load_dotenv
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import delete

load_dotenv()
url = os.environ["TEST_DATABASE_URL"]
os.environ["DATABASE_URL"] = url 

from app.db import SessionLocal
from app.models import Repo, User

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    command.upgrade(Config("alembic.ini"), "head")

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        session.execute(delete(Repo))
        session.execute(delete(User))
        session.commit()
        yield session
    finally:
        session.close()


@pytest.fixture
def auth_headers(db_session):
    register_response = client.post("/auth/register", json={"email": "test@example.com", "password": "stringisstring12"})
    assert register_response.status_code == 201
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "stringisstring12"})
    assert login_response.status_code == 200
    data = login_response.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers 
    


