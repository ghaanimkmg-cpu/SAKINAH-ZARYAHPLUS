import pytest
from app.nis.services.considered_few_service import NISConsideredFewService

def test_pipeline_strong_candidate_passes():
    # The get_considered_few uses mock_candidate_1 which is a STRONG candidate,
    # mock_candidate_blocked_age which fails hard filters,
    # and mock_candidate_weak_match which fails compatibility thresholds.
    res = NISConsideredFewService.get_considered_few("user_test")
    
    assert res.status == "HAS_CANDIDATES"
    assert len(res.candidates) == 1
    
    c = res.candidates[0]
    assert c.candidate_user_id == "demo_candidate_strong"
    assert c.confidence_level == "HIGH"
    assert c.photo_visible is False

def test_pipeline_hard_rejection_blocked():
    res = NISConsideredFewService.get_considered_few("user_test")
    # mock_candidate_blocked_age should NOT be in the results
    ids = [c.candidate_user_id for c in res.candidates]
    assert "demo_candidate_age_mismatch" not in ids

def test_pipeline_weak_compatibility_blocked():
    res = NISConsideredFewService.get_considered_few("user_test")
    # mock_candidate_weak_match should NOT be in the results
    ids = [c.candidate_user_id for c in res.candidates]
    assert "demo_candidate_weak" not in ids

def test_pipeline_privacy_fields_not_exposed():
    res = NISConsideredFewService.get_considered_few("user_test")
    dump = res.model_dump_json()
    assert "raw_raya" not in dump
    assert "swipe" not in dump
    assert "feed" not in dump
    assert "percentage" not in dump
    assert "aadhaar" not in dump.lower()

from fastapi.testclient import TestClient
from app.main import app

def test_api_route_considered_few():
    client = TestClient(app)
    # The route expects a test user header in development mode
    response = client.get("/api/v1/nis/considered-few", headers={"X-Test-User-Id": "user_frontend_dev"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HAS_CANDIDATES"
    assert len(data["candidates"]) == 1
    
    c = data["candidates"][0]
    assert c["candidate_user_id"] == "demo_candidate_strong"
    assert c["confidence_level"] == "HIGH"
    
    # Assert private fields are completely stripped
    assert "raw_raya" not in str(data)
    assert "firebase" not in str(data).lower()
