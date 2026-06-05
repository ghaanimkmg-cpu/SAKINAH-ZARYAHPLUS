from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import VerificationStatus, Gender

class NISKycVerification(NISBaseModel):
    __tablename__ = "nis_kyc_verifications"
    user_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), unique=True, nullable=False)
    verified_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    verification_status = Column(SQLEnum(VerificationStatus), default=VerificationStatus.PENDING)
    kyc_provider_reference = Column(String, nullable=True)
    identity_hash = Column(String, index=True, nullable=True)
    human_review_required = Column(Boolean, default=False)
    review_reason = Column(String, nullable=True)
