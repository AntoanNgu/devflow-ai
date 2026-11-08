from fastapi import FastAPI
from app.db import engine 
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse

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

    