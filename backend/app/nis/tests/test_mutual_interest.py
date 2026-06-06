import pytest  # type: ignore
from app.nis.services.mutual_interest_service import NISMutualInterestService
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.v1.nis.interests import router

app = FastAPI()
app.include_router(router, prefix="/api/v1/nis")
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    NISMutualInterestService.clear_mock_state()
    NISMutualInterestService.seed_mock_state(
        user_status={"user_a": "VERIFIED", "user_b": "VERIFIED", "user_banned": "BANNED", "user_1": "VERIFIED"},
        candidate_status={"cand_good": "HIGH_CONFIDENCE_MATCH", "cand_bad": "LOW_CONFIDENCE_DO_NOT_SHOW"}
    )
    yield
    NISMutualInterestService.clear_mock_state()

def test_user_can_record_private_interest():
    res = NISMutualInterestService.record_interest("user_a", "cand_good")
    assert res.status == "INTEREST_RECORDED"
    assert res.mutual_interest is False
    assert "privately" in res.message.lower()

def test_mutual_interest_is_detected():
    NISMutualInterestService.record_interest("user_a", "user_b")
    # For testing mutual, user_a must also be a valid high confidence candidate for user_b
    NISMutualInterestService.seed_mock_state({}, {"user_a": "HIGH_CONFIDENCE_MATCH"})
    res = NISMutualInterestService.record_interest("user_b", "user_a")
    assert res.status == "MUTUAL_INTEREST"
    assert res.mutual_interest is True
    assert "next step will be guided" in res.message.lower()

def test_silent_pass_is_recorded():
    res = NISMutualInterestService.record_pass("user_a", "cand_good")
    assert res.status == "PASS_RECORDED"
    assert res.mutual_interest is False
    assert "silently" in res.message.lower()

def test_duplicate_interest_handled_safely():
    NISMutualInterestService.record_interest("user_a", "cand_good")
    res = NISMutualInterestService.record_interest("user_a", "cand_good")
    assert res.status == "INTEREST_RECORDED"

def test_duplicate_pass_handled_safely():
    NISMutualInterestService.record_pass("user_a", "cand_good")
    res = NISMutualInterestService.record_pass("user_a", "cand_good")
    assert res.status == "PASS_RECORDED"

def test_pass_after_interest_cancels_safely():
    NISMutualInterestService.record_interest("user_a", "cand_good")
    res = NISMutualInterestService.record_pass("user_a", "cand_good")
    assert res.status == "PASS_RECORDED"

def test_interest_after_pass_blocked():
    NISMutualInterestService.record_pass("user_a", "cand_good")
    with pytest.raises(ValueError, match="Cannot express interest after passing."):
        NISMutualInterestService.record_interest("user_a", "cand_good")

def test_ineligible_user_blocked():
    with pytest.raises(ValueError, match="User is BANNED"):
        NISMutualInterestService.record_interest("user_banned", "cand_good")

def test_interest_only_works_for_approved_candidates():
    with pytest.raises(ValueError, match="Candidate is not approved"):
        NISMutualInterestService.record_interest("user_a", "cand_bad")

def test_no_who_liked_you_or_rejection_data():
    res = NISMutualInterestService.record_interest("user_a", "cand_good")
    dump = res.model_dump_json().lower()
    assert "rejected" not in dump
    assert "who liked you" not in dump

def test_api_express_interest():
    response = client.post("/api/v1/nis/candidates/cand_good/interest")
    assert response.status_code == 200
    assert response.json()["status"] == "INTEREST_RECORDED"

def test_api_express_pass():
    response = client.post("/api/v1/nis/candidates/cand_good/pass")
    assert response.status_code == 200
    assert response.json()["status"] == "PASS_RECORDED"
