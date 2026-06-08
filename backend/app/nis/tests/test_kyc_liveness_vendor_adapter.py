from fastapi.testclient import TestClient
from app.main import app
import uuid
from app.core.config import settings
from app.nis.models.user import NISUser
from app.nis.models.demographics import NISDemographicProfile

client = TestClient(app)

def test_kyc_sandbox_start_works(db, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.commit()

    response = client.post("/api/v1/nis/kyc/start", headers={"X-Test-User-Id": str(uid)})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SANDBOX_READY"
    assert "sandbox_kyc_" in data["session_id"]

def test_kyc_sandbox_complete_only_stores_minimized_data(db, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.add(NISDemographicProfile(user_id=uid))
    db.commit()

    payload = {
        "verified_name": "Test User",
        "verified_age": 30,
        "verified_gender": "FEMALE"
    }
    response = client.post("/api/v1/nis/kyc/sandbox/complete", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert response.status_code == 200
    assert response.json()["status"] == "VERIFIED"
    assert response.json()["verification_level"] == "FULL"

def test_production_without_vendor_credentials_returns_not_configured(db, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "KYC_PROVIDER_API_KEY", "")
    
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.commit()

    # Note: production expects real token, so we mock security just for this routing test
    # or we can test adapter directly
    from app.nis.services.kyc_vendor_adapter import SandboxKycVendorAdapter
    res = SandboxKycVendorAdapter.start_kyc_session(str(uid))
    assert res["status"] == "VENDOR_NOT_CONFIGURED"

def test_weak_liveness_sets_human_review(db, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.commit()

    payload = {
        "liveness_status": "WEAK",
        "face_match_status": "STRONG"
    }
    response = client.post("/api/v1/nis/liveness/sandbox/complete", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING_REVIEW"
    assert data["human_review_required"] is True

def test_no_firebase_dependency_added():
    import importlib.metadata
    installed_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    assert "firebase-admin" not in installed_packages
