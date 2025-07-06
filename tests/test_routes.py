from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app

client = TestClient(app)

def test_get_tickets():
    resp = client.get("/tickets")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_ticket_by_id():
    resp = client.get("/tickets/1")
    assert resp.status_code in [200, 404] 

def test_stats():
    resp = client.get("/stats")
    assert resp.status_code == 200
    assert "total" in resp.json()

def test_search_tickets():
    resp = client.get("/tickets/search?q=delectus")
    print(resp.text) 
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


