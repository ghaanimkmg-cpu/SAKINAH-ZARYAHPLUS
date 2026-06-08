import uuid
import json
from fastapi.testclient import TestClient
from app.main import app
from app.nis.models.user import NISUser

def test_niyyah_save_and_read(db, client):
    # Setup test user
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id="readiness_user_1"))
    db.commit()
    
    # Read empty
    resp = client.get("/api/v1/nis/niyyah/me", headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == False
    
    # Save Niyyah
    payload = {"intention_text": json.dumps({"whyNow": "worship", "season": "building"})}
    resp = client.put("/api/v1/nis/niyyah/me", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == True
    
    # Read populated
    resp = client.get("/api/v1/nis/niyyah/me", headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == True
    assert "worship" in resp.json()["intention_text"]

def test_values_save_and_read(db, client):
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id="readiness_user_2"))
    db.commit()
    
    # Save Values
    payload = {"values_data": {"value": "steadiness", "tradition": "sunni_hanafi"}}
    resp = client.put("/api/v1/nis/values/me", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == True
    assert resp.json()["values_data"]["value"] == "steadiness"

def test_mirror_save_and_read(db, client):
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id="readiness_user_3"))
    db.commit()
    
    payload = {"reflection_data": {"family": "A", "closeness": "B"}}
    resp = client.put("/api/v1/nis/mirror/me", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == True

def test_portrait_save_and_read(db, client):
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id="readiness_user_4"))
    db.commit()
    
    payload = {"portrait_data": {"auraChar": "ع"}}
    resp = client.put("/api/v1/nis/portrait/me", json=payload, headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["is_complete"] == True

def test_readiness_home_aggregation(db, client):
    uid = uuid.uuid4()
    db.add(NISUser(id=uid, zaryah_user_id="readiness_user_5"))
    db.commit()
    
    # Aggregation starts empty
    resp = client.get("/api/v1/nis/readiness/home", headers={"X-Test-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["niyyah_complete"] == False
    assert data["is_fully_ready"] == False
    assert "spiritual_score" not in data # Ensure no spiritual score
    
    # Complete Niyyah
    client.put("/api/v1/nis/niyyah/me", json={"intention_text": "text"}, headers={"X-Test-User-Id": str(uid)})
    
    # Check aggregation again
    resp = client.get("/api/v1/nis/readiness/home", headers={"X-Test-User-Id": str(uid)})
    data = resp.json()
    assert data["niyyah_complete"] == True
    assert data["values_complete"] == False
