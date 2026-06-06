import pytest  # type: ignore
from app.nis.services.structured_conversation_service import NISStructuredConversationService
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    NISStructuredConversationService.clear_mock_state()
    NISStructuredConversationService.seed_matchflow_state("mf_123", "STRUCTURED_OPENING")
    
    def override_get_current_user():
        return UserContext(user_id="user_a")
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    yield
    
    NISStructuredConversationService.clear_mock_state()
    app.dependency_overrides.clear()


def test_conversation_cannot_start_before_permission():
    with pytest.raises(ValueError, match="Conversation cannot start without valid matchflow permission."):
        NISStructuredConversationService.get_or_create_conversation("mf_invalid", "user_a")

def test_conversation_starts_only_after_valid_matchflow():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    assert conv_id.startswith("conv_")

def test_first_topic_is_parents_and_family():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    res = NISStructuredConversationService.get_conversation(conv_id, "user_a")
    assert res.current_topic == "PARENTS_AND_FAMILY"
    assert res.topics[0].topic == "PARENTS_AND_FAMILY"
    assert res.topics[0].status == "CURRENT"

def test_topics_unlock_one_by_one():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    NISStructuredConversationService.advance_topic(conv_id)
    res = NISStructuredConversationService.get_conversation(conv_id, "user_a")
    assert res.current_topic == "WORK"
    assert res.topics[0].status == "DONE"
    assert res.topics[1].status == "CURRENT"

def test_message_must_belong_to_current_topic():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    with pytest.raises(ValueError, match="Message must belong to the current active topic"):
        NISStructuredConversationService.post_message(conv_id, "user_a", "WORK", "hello")
        
    res = NISStructuredConversationService.post_message(conv_id, "user_a", "PARENTS_AND_FAMILY", "hello")
    assert res.accepted is True

def test_no_intimacy_topic_exists_in_prenikah():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    res = NISStructuredConversationService.get_conversation(conv_id, "user_a")
    for t in res.topics:
        assert "INTIMACY" not in t.topic
        assert "CLOSENESS" not in t.topic

def test_contact_info_phone_number_detected():
    res = NISStructuredConversationService.detect_contact_leak("my number is 1234567890")
    assert res is True

def test_contact_info_email_detected():
    res = NISStructuredConversationService.detect_contact_leak("reach me at abc@def.com")
    assert res is True

def test_social_handle_detected():
    res = NISStructuredConversationService.detect_contact_leak("my ig handle is something")
    assert res is True
    res2 = NISStructuredConversationService.detect_contact_leak("find me on instagram.com/abc")
    assert res2 is True

def test_external_link_detected():
    res = NISStructuredConversationService.detect_contact_leak("check out https://example.com")
    assert res is True

def test_call_me_dm_me_detected():
    assert NISStructuredConversationService.detect_contact_leak("hey dm me") is True
    assert NISStructuredConversationService.detect_contact_leak("call me later") is True

def test_contact_leak_message_is_rejected():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    res = NISStructuredConversationService.post_message(conv_id, "user_a", "PARENTS_AND_FAMILY", "dm me later")
    assert res.accepted is False
    assert res.contact_leak_detected is True
    
def test_raw_private_data_not_exposed():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    res = NISStructuredConversationService.get_conversation(conv_id, "user_a")
    dump = res.model_dump_json().lower()
    assert "raw_raya" not in dump
    assert "barakah" not in dump

def test_api_endpoints():
    conv_id = NISStructuredConversationService.get_or_create_conversation("mf_123", "user_a")
    NISStructuredConversationService.set_mock_users(conv_id, ["user_a", "user_b"])
    
    get_res = client.get(f"/api/v1/nis/conversations/{conv_id}")
    assert get_res.status_code == 200
    
    post_res = client.post(f"/api/v1/nis/conversations/{conv_id}/messages", json={"topic": "PARENTS_AND_FAMILY", "content": "hello families"})
    assert post_res.status_code == 200
    assert post_res.json()["accepted"] is True
