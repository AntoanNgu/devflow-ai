from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User, Repo

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

    def get_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)

        return self.db.scalar(query)

class RepoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, repo_url: str, requested_ref: str | None) -> Repo:
        new_repo = Repo(user_id=user_id, repo_url=repo_url, requested_ref=requested_ref)
        self.db.add(new_repo)
        self.db.commit()
        self.db.refresh(new_repo)
        return new_repo

