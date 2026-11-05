from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
import os

app = FastAPI(title="devflow-ai")
load_dotenv()
url = os.environ.get("DATABASE_URL")
engine = create_engine(url)

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}