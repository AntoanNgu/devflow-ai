from app.models import User
from app.repositories import UserRepository
from pwdlib import PasswordHash
from app.exceptions import EmailAlreadyRegistered, InvalidCredentials
import jwt
from datetime import datetime, timedelta, timezone


class AuthService:
    def __init__(self, users: UserRepository, hasher: PasswordHash, secret_key: str, algorithm: str, expire_minutes: int):
        self.users = users
        self.hasher = hasher
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def register(self, email: str, password: str) -> User:
        existing = self.users.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegistered
        password_hash = self.hasher.hash(password)
        return self.users.create(email, password_hash)

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email)
        if user is None:
            raise InvalidCredentials
        if not self.hasher.verify(password, user.password_hash):
            raise InvalidCredentials
        sub = str(user.id)
        exp = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        token_string = jwt.encode({"sub": sub, "exp": exp}, key=self.secret_key, algorithm=self.algorithm)
        return token_string

    

    
        



