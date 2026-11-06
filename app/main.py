from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="devflow-ai")
load_dotenv()
url = os.environ.get("DATABASE_URL")
engine = create_engine(url)


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except OperationalError:
        response = JSONResponse(status_code=503, content={"status": "error", "database": "unreachable"})
        return response

    