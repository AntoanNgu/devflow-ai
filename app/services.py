from app.models import User
from app.repositories import UserRepository
from pwdlib import PasswordHash
from app.exceptions import EmailAlreadyRegistered

class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHash):
        self.users = users
        self.hasher = hasher
        
    def register(self, email: str, password: str) -> User:
        existing = self.users.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegistered
        password_hash = self.hasher.hash(password)
        return self.users.create(email, password_hash)
        



