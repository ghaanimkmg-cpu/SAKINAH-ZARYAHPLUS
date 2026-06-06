import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.nis.models.base import NISBaseModel
from app.nis.models.user import NISUser
from app.nis.models.matching import NISMatchflow
from app.nis.models.conversation import NISStructuredConversation
from app.nis.enums.nis_enums import MatchflowStatus
from app.nis.services.structured_conversation_service import NISStructuredConversationService

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    NISBaseModel.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    NISBaseModel.metadata.drop_all(bind=engine)

def test_cannot_open_free_chat_without_correct_matchflow_state(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    mf = NISMatchflow(user_a_id=ua, user_b_id=ub, current_step="MUTUAL_INTEREST", status=MatchflowStatus.ACTIVE)
    db.add(mf)
    db.commit()

    # The service expects STRUCTURED_OPENING to create a conversation
    with pytest.raises(ValueError, match="Conversation cannot start without valid matchflow permission"):
        NISStructuredConversationService.get_or_create_conversation(db, str(mf.id), str(ua))

def test_contact_leakage_is_blocked(db):
    # This logic operates independently of DB but we test it via the service
    assert NISStructuredConversationService.detect_contact_leak("my number is 1234567890") is True
    assert NISStructuredConversationService.detect_contact_leak("dm me on ig") is True
    assert NISStructuredConversationService.detect_contact_leak("just normal text here") is False

def test_intimacy_topic_not_available_before_nikah(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    mf = NISMatchflow(user_a_id=ua, user_b_id=ub, current_step="STRUCTURED_OPENING", status=MatchflowStatus.ACTIVE)
    db.add(mf)
    db.commit()

    conv_id = NISStructuredConversationService.get_or_create_conversation(db, str(mf.id), str(ua))
    res = NISStructuredConversationService.get_conversation(db, conv_id, str(ua))
    
    for t in res.topics:
        assert "INTIMACY" not in t.topic.upper()
        assert "CLOSENESS" not in t.topic.upper()
