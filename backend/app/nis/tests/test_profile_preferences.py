import pytest  # type: ignore
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)
HEADERS = {"X-Test-User-Id": "test-user-123"}

@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")

def test_get_default_profile():
    response = client.get("/api/v1/nis/profile/me", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["emotional_steadiness"] == "UNKNOWN"

def test_update_profile_success():
    payload = {
        "emotional_steadiness": "STEADY",
        "communication_style": "DIRECT",
        "conflict_repair_style": "CALM",
        "family_responsibility": "HIGH",
        "deen_alignment": "STRONG",
        "marriage_readiness": "READY",
        "financial_expectation": "MODERATE",
        "wali_comfort": "COMFORTABLE",
        "life_direction": "ALIGNED",
        "self_awareness_level": "HIGH",
        "social_lifestyle": "BALANCED",
        "missing_signal_areas": []
    }
    response = client.put("/api/v1/nis/profile/me", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["emotional_steadiness"] == "STEADY"

def test_profile_ignores_prohibited_fields():
    payload = {
        "emotional_steadiness": "STEADY",
        "communication_style": "DIRECT",
        "conflict_repair_style": "CALM",
        "family_responsibility": "HIGH",
        "deen_alignment": "STRONG",
        "marriage_readiness": "READY",
        "financial_expectation": "MODERATE",
        "wali_comfort": "COMFORTABLE",
        "life_direction": "ALIGNED",
        "self_awareness_level": "HIGH",
        "social_lifestyle": "BALANCED",
        "raw_raya_conversation": "SECRET DATA",
        "worship_score": 99,
        "compatibility_percentage": 100
    }
    response = client.put("/api/v1/nis/profile/me", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "raw_raya_conversation" not in data
    assert "worship_score" not in data
    assert "compatibility_percentage" not in data

def test_get_default_preferences():
    response = client.get("/api/v1/nis/preferences/me", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["age_range_min"] == 18

def test_update_preferences_success():
    payload = {
        "age_range_min": 25,
        "age_range_max": 35,
        "location_preference": "USA",
        "relocation_openness": "OPEN",
        "nikah_timeline": "1_YEAR",
        "tradition_preference": "MODERN",
        "wali_involvement_preference": "MODERATE",
        "marital_status_preference": "NEVER_MARRIED",
        "financial_expectation_preference": "FLEXIBLE",
        "deal_breakers": ["SMOKING"]
    }
    response = client.put("/api/v1/nis/preferences/me", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["age_range_min"] == 25
    assert data["age_range_max"] == 35

def test_preferences_age_validation_fails():
    payload = {
        "age_range_min": 35,
        "age_range_max": 25,  # min > max
        "location_preference": "USA",
        "relocation_openness": "OPEN",
        "nikah_timeline": "1_YEAR",
        "tradition_preference": "MODERN",
        "wali_involvement_preference": "MODERATE",
        "marital_status_preference": "NEVER_MARRIED",
        "financial_expectation_preference": "FLEXIBLE"
    }
    response = client.put("/api/v1/nis/preferences/me", json=payload, headers=HEADERS)
    assert response.status_code == 422
    assert "age_range_min cannot be greater than age_range_max" in str(response.json())

def test_unauthorized_access():
    response = client.get("/api/v1/nis/profile/me")
    assert response.status_code == 401
