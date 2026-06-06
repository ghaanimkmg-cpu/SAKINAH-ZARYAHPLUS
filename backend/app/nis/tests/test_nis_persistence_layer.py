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
