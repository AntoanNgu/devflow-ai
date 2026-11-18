from app.models import User
from app.services import AuthService
from app.exceptions import EmailAlreadyRegistered
from pwdlib import PasswordHash
from app.config import Settings
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

@pytest.fixture
def auth_service():
    service = AuthService(FakeUserRepository(), PasswordHash.recommended(), secret_key="test-secret", algorithm="HS256", expire_minutes=20)
    return service
    
def test_register_returns_new_user(auth_service):
    
    user = auth_service.register("test@example.com", "hunter22")
    assert user.email == "test@example.com"
    assert user.id is not None 

def test_register_duplicate_email_raises(auth_service):
    auth_service.register("test@example.com", "hunter22")
    with pytest.raises(EmailAlreadyRegistered):
        auth_service.register("test@example.com", "hunter22")

def test_register_hashes_password(auth_service):
    user = auth_service.register("test@example.com", "hunter22")
    assert user.password_hash != "hunter22"
    assert auth_service.hasher.verify("hunter22", user.password_hash)



    





