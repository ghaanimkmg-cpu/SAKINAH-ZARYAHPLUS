import pytest
import jwt
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.nis.models.user import NISUser
import uuid

@pytest.fixture
def test_client():
    return TestClient(app)

def create_token(user_id: str, role: str = "user"):
    payload = {"sub": user_id, "role": role}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def test_production_without_authorization_rejected(test_client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    response = test_client.get("/api/v1/nis/profile/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_production_with_test_header_rejected(test_client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    response = test_client.get("/api/v1/nis/profile/me", headers={"X-Test-User-Id": "fake"})
    assert response.status_code == 401
    assert "X-Test-User-Id not allowed in production" in response.json()["detail"]

def test_development_with_test_header_works(db, client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.commit()
    
    response = client.get("/api/v1/nis/profile/me", headers={"X-Test-User-Id": str(uid)})
    assert response.status_code == 200

def test_invalid_token_rejected(test_client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    response = test_client.get("/api/v1/nis/profile/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Invalid authentication credentials" in response.json()["detail"]

def test_admin_route_rejects_normal_user(db, client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id=str(uid)))
    db.commit()
    
    response = client.get("/api/v1/nis/admin/reviews", headers={"X-Test-User-Id": str(uid)})
    assert response.status_code == 403
    assert "Admin privileges required" in response.json()["detail"]

def test_admin_route_accepts_admin_user(db, client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    uid = uuid.uuid4()
    # In our mock logic, starting with admin_ grants admin role
    admin_id = f"admin_{str(uid)}"
    db.add(NISUser(id=uid, zaryah_user_id=admin_id))
    db.commit()
    
    response = client.get("/api/v1/nis/admin/reviews", headers={"X-Test-User-Id": admin_id})
    assert response.status_code == 200

def test_no_firebase_dependency_added():
    import importlib.metadata
    installed_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
    assert "firebase-admin" not in installed_packages, "Firebase must not be installed!"
