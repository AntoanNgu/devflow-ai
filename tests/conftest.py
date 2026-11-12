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

