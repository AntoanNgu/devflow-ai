from app.models import User
from app.repositories import UserRepository

class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users
    
    def register(self, email: str, password: str) -> User: 
        ...


