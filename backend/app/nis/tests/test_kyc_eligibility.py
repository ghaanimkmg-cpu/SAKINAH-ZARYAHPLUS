import pytest  # type: ignore
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.nis.services.eligibility_service import NISEligibilityService
from app.nis.enums.nis_enums import EligibilityStatus

client = TestClient(app)
HEADERS = {"X-Test-User-Id": "test-user-123"}

@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")

def test_kyc_start():
    response = client.post("/api/v1/nis/kyc/start", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SANDBOX_READY"
    assert "session_id" in data

def test_kyc_callback_success():
    payload = {
        "verified_name": "Test User",
        "verified_age": 25,
        "verified_gender": "MALE"
    }
    response = client.post("/api/v1/nis/kyc/sandbox/complete", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "VERIFIED"
    assert data["verification_level"] == "FULL"

def test_kyc_callback_low_liveness_creates_human_review():
    payload = {
        "liveness_status": "WEAK",
        "face_match_status": "STRONG"
    }
    response = client.post("/api/v1/nis/liveness/sandbox/complete", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING_REVIEW"
    assert data["human_review_required"] is True

def test_kyc_callback_low_face_match_creates_human_review():
    payload = {
        "liveness_status": "STRONG",
        "face_match_status": "WEAK"
    }
    response = client.post("/api/v1/nis/liveness/sandbox/complete", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING_REVIEW"
    assert data["human_review_required"] is True

def test_kyc_callback_rejected():
    pass # Replaced by liveness sandbox tests"

import asyncio

def test_eligibility_service_banned():
    response = asyncio.run(NISEligibilityService.check_eligibility("test", is_banned=True))
    assert response.eligibility_status == EligibilityStatus.BANNED
    assert not response.can_enter_matching

def test_eligibility_service_pending():
    response = asyncio.run(NISEligibilityService.check_eligibility("test", kyc_status="PENDING"))
    assert response.eligibility_status == EligibilityStatus.PENDING
    assert not response.can_enter_matching

def test_eligibility_service_human_review():
    response = asyncio.run(NISEligibilityService.check_eligibility("test", kyc_status="HUMAN_REVIEW_REQUIRED"))
    assert response.eligibility_status == EligibilityStatus.HUMAN_REVIEW_REQUIRED
    assert not response.can_enter_matching
    assert response.requires_human_review

def test_eligibility_service_verified():
    response = asyncio.run(NISEligibilityService.check_eligibility("test", kyc_status="VERIFIED"))
    assert response.eligibility_status == EligibilityStatus.VERIFIED
    assert response.can_enter_matching


def test_get_eligibility_api_returns_safe_minimal_data():
    response = client.get("/api/v1/nis/eligibility/me", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "eligibility_status" in data
    assert "can_enter_matching" in data
    assert "requires_human_review" in data
    assert "message" in data
    # Ensure no raw PII fields are exposed
    assert "verified_name" not in data
    assert "age" not in data
    assert "identity_hash" not in data
