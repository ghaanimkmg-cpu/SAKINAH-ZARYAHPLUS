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
    assert data["status"] == "PENDING"
    assert data["provider"] == "sandbox"

def test_kyc_callback_success():
    payload = {
        "provider_reference": "ref-123",
        "verified_name": "Test User",
        "age": 25,
        "gender": "MALE",
        "identity_hash": "abc123hash",
        "liveness_score": 0.95,
        "face_match_score": 0.90,
        "verification_passed": True
    }
    response = client.post("/api/v1/nis/kyc/callback", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["verification_status"] == "VERIFIED"
    assert not data["human_review_required"]

def test_kyc_callback_low_liveness_creates_human_review():
    payload = {
        "provider_reference": "ref-123",
        "verified_name": "Test User",
        "age": 25,
        "gender": "MALE",
        "identity_hash": "abc123hash",
        "liveness_score": 0.75,  # Low score
        "face_match_score": 0.90,
        "verification_passed": True
    }
    response = client.post("/api/v1/nis/kyc/callback", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["verification_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["human_review_required"] is True
    assert "Low liveness score" in data["review_reason"]

def test_kyc_callback_low_face_match_creates_human_review():
    payload = {
        "provider_reference": "ref-123",
        "verified_name": "Test User",
        "age": 25,
        "gender": "MALE",
        "identity_hash": "abc123hash",
        "liveness_score": 0.95,
        "face_match_score": 0.60, # Low score
        "verification_passed": True
    }
    response = client.post("/api/v1/nis/kyc/callback", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["verification_status"] == "HUMAN_REVIEW_REQUIRED"
    assert data["human_review_required"] is True
    assert "Low face match score" in data["review_reason"]

def test_kyc_callback_rejected():
    payload = {
        "provider_reference": "ref-123",
        "verified_name": "Test User",
        "age": 25,
        "gender": "MALE",
        "identity_hash": "abc123hash",
        "liveness_score": 0.95,
        "face_match_score": 0.95,
        "verification_passed": False
    }
    response = client.post("/api/v1/nis/kyc/callback", json=payload, headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["verification_status"] == "REJECTED"

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
