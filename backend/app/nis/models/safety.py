from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import SafetyFlagType, SafetySeverity, HumanReviewStatus, HumanReviewDecision

class NISSafetyFlag(NISBaseModel):
    __tablename__ = "nis_safety_flags"
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    flag_type = Column(SQLEnum(SafetyFlagType), nullable=False)
    severity = Column(SQLEnum(SafetySeverity), nullable=False)
    description = Column(Text, nullable=True)

class NISReport(NISBaseModel):
    __tablename__ = "nis_reports"
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    reason = Column(String, nullable=False)

class NISHumanReview(NISBaseModel):
    __tablename__ = "nis_human_reviews"
    report_id = Column(UUID(as_uuid=True), ForeignKey("nis_reports.id"), nullable=True)
    kyc_id = Column(UUID(as_uuid=True), ForeignKey("nis_kyc_verifications.id"), nullable=True)
    status = Column(SQLEnum(HumanReviewStatus), default=HumanReviewStatus.PENDING)
    decision = Column(SQLEnum(HumanReviewDecision), nullable=True)

class NISIdentityBan(NISBaseModel):
    __tablename__ = "nis_identity_bans"
    identity_hash = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=False)

class NISAuditLog(NISBaseModel):
    __tablename__ = "nis_audit_logs"
    action = Column(String, nullable=False)
    actor_id = Column(String, nullable=True)
    target_id = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
