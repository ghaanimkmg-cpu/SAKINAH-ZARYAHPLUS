from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Boolean, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import SafetyRiskLevel, ConfidenceLevel

class NISUserSignalProfile(NISBaseModel):
    __tablename__ = "nis_user_signal_profiles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), unique=True, nullable=False)
    emotional_steadiness = Column(Float, nullable=True)
    communication_style = Column(String, nullable=True)
    conflict_repair_style = Column(String, nullable=True)
    family_responsibility = Column(String, nullable=True)
    deen_alignment = Column(String, nullable=True)
    marriage_readiness = Column(Float, nullable=True)
    financial_expectation = Column(String, nullable=True)
    wali_comfort = Column(String, nullable=True)
    life_direction = Column(String, nullable=True)
    self_awareness_level = Column(Float, nullable=True)
    social_lifestyle = Column(String, nullable=True)
    safety_risk_level = Column(SQLEnum(SafetyRiskLevel), default=SafetyRiskLevel.LOW)
    confidence_level = Column(SQLEnum(ConfidenceLevel), default=ConfidenceLevel.LOW)
    missing_signal_areas = Column(JSON, nullable=True)
    review_required = Column(Boolean, default=False)
