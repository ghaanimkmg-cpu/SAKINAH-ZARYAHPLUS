import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.nis.models.base import NISBaseModel
from app.nis.models.user import NISUser
from app.nis.models.safety import NISSafetyFlag, NISHumanReview, NISReport
from app.nis.enums.nis_enums import SafetySeverity, HumanReviewStatus
from app.nis.schemas.safety import ReportRequest
from app.nis.services.safety_service import NISSafetyService
from app.nis.services.human_review_service import NISHumanReviewService

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    NISBaseModel.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    NISBaseModel.metadata.drop_all(bind=engine)

def test_report_creates_review_for_high_severity(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="reporter"), NISUser(id=ub, zaryah_user_id="reported")])
    db.commit()

    req = ReportRequest(reported_user_id=str(ub), flag_type="MANIPULATION_RISK", severity="HIGH")
    res = NISSafetyService.submit_report(db, str(ua), req)
    
    assert res.human_review_required is True
    
    review = db.query(NISHumanReview).filter_by(user_id=ub).first()
    assert review is not None
    assert review.status == HumanReviewStatus.PENDING

def test_banned_user_is_blocked(db):
    ua = uuid.uuid4()
    db.add(NISUser(id=ua, zaryah_user_id="bad_user"))
    db.commit()
    
    # We simulate a PERMANENT_BAN decision creating an identity ban
    from app.nis.schemas.human_review import ReviewDecisionRequest
    # Insert a dummy review
    rev = NISHumanReview(user_id=ua, status=HumanReviewStatus.PENDING)
    db.add(rev)
    db.commit()

    NISHumanReviewService.submit_decision(db, str(rev.id), ReviewDecisionRequest(decision="PERMANENT_BAN"), "admin")
    
    is_eligible = NISHumanReviewService.check_matchmaking_eligibility(db, str(ua))
    assert is_eligible is False

def test_reporter_identity_is_not_exposed(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="secret_reporter"), NISUser(id=ub, zaryah_user_id="reported")])
    db.commit()

    req = ReportRequest(reported_user_id=str(ub), flag_type="AGGRESSIVE_LANGUAGE", severity="LOW")
    res = NISSafetyService.submit_report(db, str(ua), req)
    
    dump = res.model_dump_json()
    assert str(ua) not in dump
    assert "secret_reporter" not in dump
