from app.models import User
from app.services import AuthService
from app.exceptions import EmailAlreadyRegistered
from pwdlib import PasswordHash
import pytest

class FakeUserRepository:
    def __init__(self):
        self.user_by_email = {}
        self.next_id = 1

    def get_by_email(self, email):
        return self.user_by_email.get(email)

    def create(self, email, password_hash):
        new_user = User(email=email, password_hash=password_hash)
        new_user.id = self.next_id
        self.next_id += 1
        self.user_by_email[email] = new_user
        return new_user


service = AuthService(FakeUserRepository(), PasswordHash.recommended())

def test_register_returns_new_user():
    service = AuthService(FakeUserRepository(), PasswordHash.recommended())
    user = service.register("test@example.com", "hunter22")
    assert user.email == "test@example.com"
    assert user.id is not None 
    





