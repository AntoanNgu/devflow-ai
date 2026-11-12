from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        
        return self.db.scalar(query)

    def create(self, email: str, password_hash: str) -> User:
        new_user = User(email=email, password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
        

