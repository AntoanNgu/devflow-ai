from fastapi import FastAPI, Depends, HTTPException
from app.db import engine, get_db 
from app.schemas import RegisterRequest, UserResponse, LoginRequest, TokenResponse, RepoResponse, RepoCreate
from app.repositories import UserRepository, RepoRepository
from app.services import AuthService
from app.exceptions import EmailAlreadyRegistered, InvalidCredentials
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app.config import settings
from app.dependencies import get_current_user
from app.models import User

app = FastAPI(title="devflow-ai")

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except OperationalError:
        response = JSONResponse(status_code=503, content={"status": "error", "database": "unreachable"})
        return response

@app.post("/auth/register", status_code=201, response_model=UserResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db), PasswordHash.recommended(), secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm, expire_minutes=settings.access_token_expire_minutes)
    try:
        return service.register(body.email, body.password)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=409, detail="Email already registered")

@app.post("/auth/login", status_code=200, response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db), PasswordHash.recommended(), secret_key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm, expire_minutes=settings.access_token_expire_minutes)
    try:
        token = service.login(body.email, body.password)
        return TokenResponse(access_token=token)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

@app.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/repos", status_code=201, response_model=RepoResponse)
def create_repo(body: RepoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RepoRepository(db).create(current_user.id, body.repo_url, body.requested_ref)

    