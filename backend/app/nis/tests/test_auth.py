import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_auth_missing_header_dev_mode(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    response = client.get("/api/v1/nis/auth/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_auth_with_header_dev_mode(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    response = client.get("/api/v1/nis/auth/me", headers={"X-Test-User-Id": "test-user-123"})
    assert response.status_code == 200
    assert response.json()["user_id"] == "test-user-123"

def test_auth_production_mode_not_implemented(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    response = client.get("/api/v1/nis/auth/me", headers={"X-Test-User-Id": "test-user-123"})
    assert response.status_code == 501
    assert "Production authentication integration is pending" in response.json()["detail"]
