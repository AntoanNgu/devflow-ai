from sqlalchemy.orm import Session 
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        ...
    def create(self, email: str, password_hash: str) -> User:
        ...


