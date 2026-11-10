from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app 
import app.main as main_module

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_db_unreachable(monkeypatch):
    broken_engine = create_engine("postgresql+psycopg://user:pass@localhost:1/nowhere")
    monkeypatch.setattr(main_module, "engine", broken_engine)
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "unreachable"}
