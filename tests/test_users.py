from fastapi.testclient import TestClient
from ..fastapicomplete.app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.status_code)
