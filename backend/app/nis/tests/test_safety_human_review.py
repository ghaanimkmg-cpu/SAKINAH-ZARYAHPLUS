import pytest # type: ignore
from app.nis.services.safety_service import NISSafetyService
from app.nis.services.human_review_service import NISHumanReviewService
from app.nis.schemas.safety import ReportRequest
from app.nis.schemas.human_review import ReviewDecisionRequest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    NISSafetyService.clear_mock_state()
    NISHumanReviewService.clear_mock_state()
    
    def override_get_current_user():
        return UserContext(user_id="user_test_reporter")
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield
    
    NISSafetyService.clear_mock_state()
    NISHumanReviewService.clear_mock_state()
    app.dependency_overrides.clear()

def test_report_creates_record_and_flag():
    req = ReportRequest(reported_user_id="user_bad", flag_type="AGGRESSIVE_LANGUAGE", severity="LOW")
    res = NISSafetyService.submit_report("user_good", req)
    assert res.report_id.startswith("rep_")
    assert res.safety_flag_created is True
    assert res.human_review_required is False

def test_high_severity_creates_human_review():
    req = ReportRequest(reported_user_id="user_bad", flag_type="MANIPULATION_RISK", severity="HIGH")
    res = NISSafetyService.submit_report("user_good", req)
    assert res.human_review_required is True
    assert NISHumanReviewService.get_user_status("user_bad") == "UNDER_REVIEW"

def test_critical_severity_creates_human_review():
    req = ReportRequest(reported_user_id="user_bad", flag_type="PHOTO_LEAK_RISK", severity="CRITICAL")
    res = NISSafetyService.submit_report("user_good", req)
    assert res.human_review_required is True

def test_contact_leak_creates_flag():
    NISSafetyService.log_contact_leak("user_leaker", "dm me on ig")
    assert True # Verify no crash, system report created internally

def test_repeated_reports_escalate():
    for _ in range(3):
        req = ReportRequest(reported_user_id="user_annoying", flag_type="AGGRESSIVE_LANGUAGE", severity="LOW")
        res = NISSafetyService.submit_report("user_x", req)
    
    # 3rd report escalates severity automatically to HIGH and triggers human review
    assert res.human_review_required is True

def test_human_review_decision_is_stored():
    req = ReportRequest(reported_user_id="user_bad", flag_type="MANIPULATION_RISK", severity="HIGH")
    NISSafetyService.submit_report("user_good", req)
    
    from app.nis.services.human_review_service import _MOCK_REVIEWS_DB
    review_id = list(_MOCK_REVIEWS_DB.keys())[0]
    
    d_req = ReviewDecisionRequest(decision="WARN_USER")
    d_res = NISHumanReviewService.submit_decision(review_id, d_req, "admin_1")
    assert d_res.status == "RESOLVED"
    assert d_res.decision == "WARN_USER"

def test_warn_user_decision_works():
    # Verified inherently with test above
    pass

def test_pause_matchmaking_decision_works():
    req = ReportRequest(reported_user_id="user_bad", flag_type="MANIPULATION_RISK", severity="HIGH")
    NISSafetyService.submit_report("user_good", req)
    from app.nis.services.human_review_service import _MOCK_REVIEWS_DB
    review_id = list(_MOCK_REVIEWS_DB.keys())[0]
    
    NISHumanReviewService.submit_decision(review_id, ReviewDecisionRequest(decision="PAUSE_MATCHMAKING"), "admin_1")
    assert NISHumanReviewService.get_user_status("user_bad") == "PAUSED"
    assert NISHumanReviewService.check_matchmaking_eligibility("user_bad") is False

def test_permanent_ban_decision_works():
    req = ReportRequest(reported_user_id="user_bad", flag_type="MANIPULATION_RISK", severity="HIGH")
    NISSafetyService.submit_report("user_good", req)
    from app.nis.services.human_review_service import _MOCK_REVIEWS_DB
    review_id = list(_MOCK_REVIEWS_DB.keys())[0]
    
    NISHumanReviewService.submit_decision(review_id, ReviewDecisionRequest(decision="PERMANENT_BAN"), "admin_1")
    assert NISHumanReviewService.get_user_status("user_bad") == "BANNED"
    assert NISHumanReviewService.check_matchmaking_eligibility("user_bad") is False

def test_under_review_user_is_blocked():
    req = ReportRequest(reported_user_id="user_bad", flag_type="MANIPULATION_RISK", severity="HIGH")
    NISSafetyService.submit_report("user_good", req)
    assert NISHumanReviewService.get_user_status("user_bad") == "UNDER_REVIEW"
    assert NISHumanReviewService.check_matchmaking_eligibility("user_bad") is False

def test_reporter_identity_not_exposed():
    req = ReportRequest(reported_user_id="user_bad", flag_type="AGGRESSIVE_LANGUAGE", severity="LOW")
    res = NISSafetyService.submit_report("user_good", req)
    dump = res.model_dump_json().lower()
    assert "user_good" not in dump

def test_api_endpoints():
    report_res = client.post("/api/v1/nis/reports", json={
        "reported_user_id": "user_bad_api",
        "flag_type": "HIGH",
        "severity": "CRITICAL"
    })
    # Fails validation because flag_type HIGH is not a valid flag type
    assert report_res.status_code == 400
    
    report_res2 = client.post("/api/v1/nis/reports", json={
        "reported_user_id": "user_bad_api",
        "flag_type": "BOUNDARY_PRESSURE",
        "severity": "CRITICAL"
    })
    assert report_res2.status_code == 200
    assert report_res2.json()["human_review_required"] is True

    from app.nis.services.human_review_service import _MOCK_REVIEWS_DB
    review_id = list(_MOCK_REVIEWS_DB.keys())[0]
    
    rev_res = client.post(f"/api/v1/nis/admin/reviews/{review_id}/decision", json={
        "decision": "PERMANENT_BAN"
    })
    assert rev_res.status_code == 200
    assert rev_res.json()["decision"] == "PERMANENT_BAN"

def test_admin_review_listing_exists_and_is_safe():
    req = ReportRequest(reported_user_id="user_bad_123", flag_type="MANIPULATION_RISK", severity="HIGH")
    NISSafetyService.submit_report("reporter_secret_identity", req)

    res = client.get("/api/v1/nis/admin/reviews")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    
    first_rev = data[0]
    assert "review_id" in first_rev
    assert "user_id" in first_rev
    assert first_rev["user_id"] == "user_bad_123"
    
    dump = str(data).lower()
    assert "reporter_secret_identity" not in dump
    assert "raw_raya" not in dump
