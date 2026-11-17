from fastapi import FastAPI, Depends, HTTPException
from app.db import engine, get_db 
from app.schemas import RegisterRequest, UserResponse
from app.repositories import UserRepository
from app.services import AuthService
from app.exceptions import EmailAlreadyRegistered
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

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
    service = AuthService(UserRepository(db), PasswordHash.recommended())
    try:
        return service.register(body.email, body.password)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=409, detail="Email already registered")

    