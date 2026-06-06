import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

def test_proof_endpoint_works_in_development():
    # Force development mode for the test
    settings.APP_ENV = "development"
    client = TestClient(app)
    response = client.get("/api/v1/nis/dev/proof-report")
    assert response.status_code == 200
    data = response.json()
    assert data["current_user"] == "demo_user_ayman"
    assert data["nis_passed"] is True
    
    # Check outcomes
    results = data["results"]
    assert len(results) == 6
    for r in results:
        if r["candidate_id"] == "demo_candidate_strong":
            assert r["expected"] == "SHOWN"
            assert r["actual"] == "SHOWN"
        else:
            assert r["expected"] == "BLOCKED"
            assert r["actual"] == "BLOCKED"

def test_proof_endpoint_blocked_in_production():
    settings.APP_ENV = "production"
    client = TestClient(app)
    response = client.get("/api/v1/nis/dev/proof-report")
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]
    
    # Restore dev mode for other tests
    settings.APP_ENV = "development"

def test_no_private_fields_exposed():
    client = TestClient(app)
    response = client.get("/api/v1/nis/dev/proof-report")
    data_str = response.text.lower()
    assert "percentage" not in data_str
    assert "perfect match" not in data_str
    assert "guaranteed" not in data_str
    assert "aadhaar" not in data_str
    assert "firebase" not in data_str
    assert "raw_raya" not in data_str

def test_considered_few_route_verification():
    client = TestClient(app)
    response = client.get("/api/v1/nis/considered-few", headers={"X-Test-User-Id": "demo_user_ayman"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HAS_CANDIDATES"
    
    # Only the strong candidate should be present
    assert len(data["candidates"]) == 1
    c = data["candidates"][0]
    assert c["candidate_user_id"] == "demo_candidate_strong"
    assert c["confidence_level"] == "HIGH"
