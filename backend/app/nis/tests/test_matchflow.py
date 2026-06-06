import pytest
pytestmark = pytest.mark.skip(reason="Needs rewrite for DB persistence")
from app.nis.services.matchflow_service import NISMatchflowService
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    NISMatchflowService.clear_mock_state()
    NISMatchflowService.seed_mutual_interest("user_a", "user_b")
    
    def override_get_current_user():
        return UserContext(user_id="user_a")
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield
    
    NISMatchflowService.clear_mock_state()
    app.dependency_overrides.clear()

def test_matchflow_created_only_after_mutual_interest():
    # Valid
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    assert mf_id.startswith("mf_")

    # Invalid (no mutual interest)
    with pytest.raises(ValueError, match="can only be created after mutual interest"):
        NISMatchflowService.create_matchflow("user_x", "user_y")

def test_current_step_returned_safely():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    res = NISMatchflowService.get_matchflow(mf_id, "user_a")
    assert res.current_step == "MUTUAL_INTEREST"
    assert res.chat_open is False

def test_step_list_includes_done_current_locked():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    res = NISMatchflowService.get_matchflow(mf_id, "user_a")
    
    # PROFILES_COMPLETE should be DONE
    assert res.steps[0].step == "PROFILES_COMPLETE"
    assert res.steps[0].status == "DONE"
    
    # MUTUAL_INTEREST should be CURRENT
    assert res.steps[2].step == "MUTUAL_INTEREST"
    assert res.steps[2].status == "CURRENT"
    
    # STRUCTURED_OPENING should be LOCKED
    assert res.steps[3].step == "STRUCTURED_OPENING"
    assert res.steps[3].status == "LOCKED"

def test_invalid_transition_rejected():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    # Jumping to end
    with pytest.raises(ValueError, match="Invalid state transition sequence"):
        NISMatchflowService.transition_step(mf_id, "DECISION")
    
    # Invalid step name
    with pytest.raises(ValueError, match="Invalid transition step"):
        NISMatchflowService.transition_step(mf_id, "SOMETHING_FAKE")

def test_valid_transition_works():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    NISMatchflowService.transition_step(mf_id, "STRUCTURED_OPENING")
    
    res = NISMatchflowService.get_matchflow(mf_id, "user_a")
    assert res.current_step == "STRUCTURED_OPENING"
    assert res.steps[2].status == "DONE"  # MUTUAL_INTEREST
    assert res.steps[3].status == "CURRENT" # STRUCTURED_OPENING

def test_chat_not_opened_automatically():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    res = NISMatchflowService.get_matchflow(mf_id, "user_a")
    assert res.chat_open is False

def test_raw_private_data_not_exposed():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    res = NISMatchflowService.get_matchflow(mf_id, "user_a")
    dump = res.model_dump_json().lower()
    assert "raw_raya" not in dump
    assert "barakah" not in dump
    assert "marry" not in dump
    assert "marriage" not in dump

def test_api_endpoint_matchflow():
    mf_id = NISMatchflowService.create_matchflow("user_a", "user_b")
    response = client.get(f"/api/v1/nis/matchflows/{mf_id}")
    assert response.status_code == 200
    assert response.json()["matchflow_id"] == mf_id
    assert response.json()["current_step"] == "MUTUAL_INTEREST"
