from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_repo_returns_pending(auth_headers):
    create_response = client.post("/repos",json={"repo_url": "https://github.com/theskumar/python-dotenv", "requested_ref": "v1.2.4"} ,headers=auth_headers)
    data = create_response.json()
    assert create_response.status_code == 201
    assert data["status"] == "pending"
    assert data["repo_url"] == "github.com/theskumar/python-dotenv"
    assert data["requested_ref"] == "v1.2.4"

def test_bad_url_format(auth_headers):
    create_response = client.post("/repos",json={"repo_url": "https://github.com/AntoanNgu"} ,headers=auth_headers)
    assert create_response.status_code == 422
    assert create_response.json()["detail"][0]["loc"] == ["body", "repo_url"]

def test_no_token():
    create_response = client.post("/repos",json={"repo_url": "https://github.com/theskumar/python-dotenv", "requested_ref": "v1.2.4"})
    assert create_response.status_code == 401
    assert create_response.json()["detail"] == "Could not validate credentials"




    
