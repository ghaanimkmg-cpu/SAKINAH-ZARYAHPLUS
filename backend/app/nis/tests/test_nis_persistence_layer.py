import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.nis.models.base import NISBaseModel
from app.nis.models.user import NISUser
from app.nis.models.profiles import NISUserSignalProfile
from app.nis.services.user_signal_profile_service import NISUserSignalProfileService
from app.nis.schemas.user_signal_profile import UserSignalProfile

# Use an in-memory SQLite for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    NISBaseModel.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    NISBaseModel.metadata.drop_all(bind=engine)

def test_user_signal_profile_persistence(db):
    user_id = uuid.uuid4()
    # Create user first to satisfy foreign key
    test_user = NISUser(id=user_id, zaryah_user_id="test_zaryah_id")
    db.add(test_user)
    db.commit()

    profile_data = UserSignalProfile(
        emotional_steadiness="HIGH",
        conflict_repair_style="CALM",
        communication_style="DIRECT",
        family_responsibility="HIGH",
        deen_alignment="HIGH",
        marriage_readiness="HIGH",
        financial_expectation="MODERATE",
        wali_comfort="YES",
        life_direction="CLEAR",
        self_awareness_level="HIGH",
        social_lifestyle="QUIET"
    )

    # Test Create
    result = NISUserSignalProfileService.update_profile(db, str(user_id), profile_data)
    assert result.emotional_steadiness == "HIGH"
    assert result.communication_style == "DIRECT"

    # Test Fetch
    fetched = NISUserSignalProfileService.get_profile(db, str(user_id))
    assert fetched.emotional_steadiness == "HIGH"
    assert fetched.communication_style == "DIRECT"

    # Test Fetch Default
    fetched_default = NISUserSignalProfileService.get_profile(db, str(uuid.uuid4()))
    assert fetched_default.emotional_steadiness == "UNKNOWN"

from app.nis.models.preferences import NISMatchPreference
from app.nis.models.matching import NISMatchflow, NISMatchInterest
from app.nis.models.conversation import NISStructuredConversation, NISConversationMessage
from app.nis.models.safety import NISSafetyFlag, NISHumanReview
from app.nis.enums.nis_enums import MatchflowStatus, MatchInterestStatus, SafetySeverity, SafetyRiskLevel, HumanReviewStatus, HumanReviewDecision, SafetyFlagType

def test_full_nis_persistence_layer(db):
    user_a_id = uuid.uuid4()
    user_b_id = uuid.uuid4()
    user_a = NISUser(id=user_a_id, zaryah_user_id="user_a")
    user_b = NISUser(id=user_b_id, zaryah_user_id="user_b")
    db.add(user_a)
    db.add(user_b)
    db.commit()

    # Preferences
    pref = NISMatchPreference(user_id=user_a_id, age_range_min=20, age_range_max=30)
    db.add(pref)
    db.commit()
    assert db.query(NISMatchPreference).filter_by(user_id=user_a_id).first().age_range_min == 20

    # Mutual Interest
    interest = NISMatchInterest(sender_id=user_a_id, receiver_id=user_b_id, status=MatchInterestStatus.ACCEPTED)
    db.add(interest)
    db.commit()
    assert db.query(NISMatchInterest).filter_by(sender_id=user_a_id).first().status == MatchInterestStatus.ACCEPTED

    # Matchflow
    mf = NISMatchflow(user_a_id=user_a_id, user_b_id=user_b_id, status=MatchflowStatus.ACTIVE, current_step="MUTUAL_INTEREST")
    db.add(mf)
    db.commit()
    assert db.query(NISMatchflow).first().current_step == "MUTUAL_INTEREST"

    # Conversation
    conv = NISStructuredConversation(matchflow_id=mf.id, topic_unlocked="PARENTS_AND_FAMILY")
    db.add(conv)
    db.commit()
    
    msg = NISConversationMessage(conversation_id=conv.id, sender_id=user_a_id, content="Hello", is_system_message=False)
    db.add(msg)
    db.commit()
    assert db.query(NISConversationMessage).first().content == "Hello"

    # Safety Report
    report = NISSafetyFlag(reporter_id=user_a_id, target_id=user_b_id, flag_type=SafetyFlagType.INAPPROPRIATE, severity=SafetySeverity.HIGH)
    db.add(report)
    db.commit()
    assert db.query(NISSafetyFlag).first().severity == SafetySeverity.HIGH

    # Human Review
    # We need an NISReport first to link NISHumanReview, but report_id is nullable
    review = NISHumanReview(status=HumanReviewStatus.COMPLETED, decision=HumanReviewDecision.APPROVED)
    db.add(review)
    db.commit()
    assert db.query(NISHumanReview).first().decision == HumanReviewDecision.APPROVED

    # Niyyah, Values, Mirror, Portrait (represented in models)
    from app.nis.models.profiles import NISNiyyahIntention, NISValuesProfile, NISMirrorReflection, NISPrivatePortrait
    
    niyyah = NISNiyyahIntention(user_id=user_a_id, intention_text="To complete my deen")
    values = NISValuesProfile(user_id=user_a_id, values_data={"religious_practice": "STRONG"})
    mirror = NISMirrorReflection(user_id=user_a_id, reflection_data={"self_description": "Kind"})
    portrait = NISPrivatePortrait(user_id=user_a_id, portrait_data={"family_background": "Good"})
    
    db.add_all([niyyah, values, mirror, portrait])
    db.commit()
    
    assert db.query(NISNiyyahIntention).first().intention_text == "To complete my deen"
    assert db.query(NISValuesProfile).first().values_data["religious_practice"] == "STRONG"
    assert db.query(NISMirrorReflection).first().reflection_data["self_description"] == "Kind"
    assert db.query(NISPrivatePortrait).first().portrait_data["family_background"] == "Good"
