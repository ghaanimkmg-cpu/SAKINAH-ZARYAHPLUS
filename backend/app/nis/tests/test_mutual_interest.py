import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.nis.models.base import NISBaseModel
from app.nis.models.user import NISUser
from app.nis.models.matching import NISMatchInterest, NISMatchflow
from app.nis.enums.nis_enums import MatchInterestStatus
from app.nis.services.mutual_interest_service import NISMutualInterestService

engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    NISBaseModel.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    NISBaseModel.metadata.drop_all(bind=engine)

def test_one_sided_interest_stays_private(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    res = NISMutualInterestService.record_interest(db, str(ua), str(ub))
    assert res.status == "INTEREST_RECORDED"
    assert res.mutual_interest is False
    
    interest = db.query(NISMatchInterest).filter_by(sender_id=ua, receiver_id=ub).first()
    assert interest.status == MatchInterestStatus.INTERESTED

def test_mutual_interest_unlocks_matchflow_path(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    # B likes A first
    NISMutualInterestService.record_interest(db, str(ub), str(ua))
    
    # A likes B
    res = NISMutualInterestService.record_interest(db, str(ua), str(ub))
    assert res.status == "MUTUAL_INTEREST"
    assert res.mutual_interest is True

def test_pass_is_silent(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    res = NISMutualInterestService.record_pass(db, str(ua), str(ub))
    assert res.status == "PASS_RECORDED"
    
    interest = db.query(NISMatchInterest).filter_by(sender_id=ua, receiver_id=ub).first()
    assert interest.status == MatchInterestStatus.PASSED

def test_interest_after_pass_is_blocked(db):
    ua = uuid.uuid4()
    ub = uuid.uuid4()
    db.add_all([NISUser(id=ua, zaryah_user_id="a"), NISUser(id=ub, zaryah_user_id="b")])
    db.commit()

    NISMutualInterestService.record_pass(db, str(ua), str(ub))
    
    with pytest.raises(ValueError, match="Cannot express interest after passing"):
        NISMutualInterestService.record_interest(db, str(ua), str(ub))
