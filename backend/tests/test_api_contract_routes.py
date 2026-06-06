import pytest  # type: ignore
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openapi_schema_loads():
    # 1. OpenAPI schema loads
    res = client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    assert "paths" in schema
    return schema

def test_important_endpoints_exist():
    # We inspect the actual FastAPI routes
    routes = [route.path for route in app.routes]
    
    # 7. Health endpoints
    assert "/health" in routes
    assert "/api/v1/health" in routes
    
    # Auth
    assert "/api/v1/nis/auth/me" in routes
    
    # KYC
    assert "/api/v1/nis/kyc/start" in routes
    assert "/api/v1/nis/kyc/callback" in routes
    assert "/api/v1/nis/eligibility/me" in routes
    
    # Profile / Preferences
    assert "/api/v1/nis/profile/me" in routes
    assert "/api/v1/nis/preferences/me" in routes
    
    # Considered Few
    assert "/api/v1/nis/considered-few" in routes

    # 4. Interest/pass/candidate endpoints exist
    assert "/api/v1/nis/candidates/{candidate_id}" in routes
    assert "/api/v1/nis/candidates/{candidate_id}/interest" in routes
    assert "/api/v1/nis/candidates/{candidate_id}/pass" in routes
    
    # Matchflow
    assert "/api/v1/nis/matchflows/{matchflow_id}" in routes
    assert "/api/v1/nis/matchflows/{matchflow_id}/decision" in routes
    
    # 5. Conversation endpoints exist
    assert "/api/v1/nis/conversations/{conversation_id}" in routes
    assert "/api/v1/nis/conversations/{conversation_id}/messages" in routes
    
    # 6. Report endpoint exists
    assert "/api/v1/nis/reports" in routes
    
    # 3. Admin review listing endpoint exists
    assert "/api/v1/nis/admin/reviews" in routes
    assert "/api/v1/nis/admin/reviews/{review_id}/decision" in routes

def test_no_firebase_dependency_introduced():
    # 8. No Firebase dependency is introduced
    import sys
    assert "firebase_admin" not in sys.modules
