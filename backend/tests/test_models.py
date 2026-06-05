import os
from app.core.database import Base

# Import all models to test imports and metadata registration
from app.nis.models import *
from app.nis.enums.nis_enums import *
from app.nis.models.kyc import NISKycVerification
from app.nis.models.profiles import NISUserSignalProfile
from app.nis.models.safety import NISAuditLog

def test_all_models_registered():
    # Verify all 15 tables are in the metadata
    tables = Base.metadata.tables.keys()
    required_tables = [
        "nis_users",
        "nis_kyc_verifications",
        "nis_match_preferences",
        "nis_user_signal_profiles",
        "nis_compatibility_evaluations",
        "nis_considered_pools",
        "nis_match_interests",
        "nis_matchflows",
        "nis_structured_conversations",
        "nis_conversation_messages",
        "nis_safety_flags",
        "nis_reports",
        "nis_human_reviews",
        "nis_identity_bans",
        "nis_audit_logs"
    ]
    for table in required_tables:
        assert table in tables, f"Table {table} is missing from metadata"

def test_kyc_model_no_prohibited_fields():
    columns = [c.name for c in NISKycVerification.__table__.columns]
    prohibited = ["aadhaar", "government_id", "id_image", "selfie"]
    for p in prohibited:
        assert p not in columns

def test_profile_model_no_prohibited_fields():
    columns = [c.name for c in NISUserSignalProfile.__table__.columns]
    prohibited = ["raya", "barakah", "worship_score", "gratitude_score", "public_spiritual_score"]
    for p in prohibited:
        assert p not in columns

def test_audit_log_exists():
    assert "nis_audit_logs" in Base.metadata.tables.keys()

def test_enums_import():
    assert hasattr(VerificationStatus, "PENDING")
    assert hasattr(Gender, "MALE")
    assert hasattr(SafetyRiskLevel, "LOW")

def test_alembic_migration_file_exists():
    # Alembic creates migrations in backend/alembic/versions
    versions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic", "versions")
    assert os.path.isdir(versions_dir)
    # Check if any .py files exist inside versions
    migration_files = [f for f in os.listdir(versions_dir) if f.endswith(".py")]
    assert len(migration_files) > 0, "No alembic migration file found"
