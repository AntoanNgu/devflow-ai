import jwt 
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import settings 
from app.db import get_db 
from app.models import User
from app.repositories import UserRepository

bearer = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload["sub"]
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = UserRepository(db).get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user 

    


