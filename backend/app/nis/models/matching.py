from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import CompatibilityStatus, MatchInterestStatus, MatchflowStatus

class NISCompatibilityEvaluation(NISBaseModel):
    __tablename__ = "nis_compatibility_evaluations"
    user_a_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    user_b_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    compatibility_score = Column(Float, nullable=True)
    compatibility_status = Column(SQLEnum(CompatibilityStatus), nullable=True)
    evaluation_reasons = Column(JSON, nullable=True)

class NISConsideredPool(NISBaseModel):
    __tablename__ = "nis_considered_pools"
    user_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    pool_status = Column(String, nullable=True)
    score = Column(Float, nullable=True)

class NISMatchInterest(NISBaseModel):
    __tablename__ = "nis_match_interests"
    sender_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    status = Column(SQLEnum(MatchInterestStatus), default=MatchInterestStatus.PENDING)

class NISMatchflow(NISBaseModel):
    __tablename__ = "nis_matchflows"
    user_a_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    user_b_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), nullable=False)
    status = Column(SQLEnum(MatchflowStatus), default=MatchflowStatus.PENDING)
    current_step = Column(String, nullable=True)
