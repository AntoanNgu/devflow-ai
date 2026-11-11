import os
from dotenv import load_dotenv
import pytest
from alembic import command
from alembic.config import Config

load_dotenv()
url = os.environ["TEST_DATABASE_URL"]
os.environ["DATABASE_URL"] = url 

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    command.upgrade(Config("alembic.ini"), "head")