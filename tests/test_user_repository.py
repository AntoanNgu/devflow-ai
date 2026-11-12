from app.repositories import UserRepository

def test_create_user_with_id(db_session):
    repo = UserRepository(db_session)
    user = repo.create(email="test@example.com", password_hash="abc123")
    assert user.id is not None 
    assert user.email == "test@example.com" 
    

def test_get_by_email_finds_existing_user(db_session):
    repo = UserRepository(db_session)
    user = repo.create(email="test@example.com", password_hash="abc123")
    found = repo.get_by_email(email="test@example.com")
    assert user.id == found.id
    assert found.id is not None

def test_get_by_email_returns_none_for_unknown_email(db_session):
    repo = UserRepository(db_session)
    found = repo.get_by_email(email="nobody@example.com")
    assert found is None
    