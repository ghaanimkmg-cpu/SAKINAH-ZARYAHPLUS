from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel

class NISMatchPreference(NISBaseModel):
    __tablename__ = "nis_match_preferences"
    user_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), unique=True, nullable=False)
    age_range_min = Column(Integer, nullable=True)
    age_range_max = Column(Integer, nullable=True)
    location_preference = Column(String, nullable=True)
    relocation_openness = Column(Boolean, nullable=True)
    nikah_timeline = Column(String, nullable=True)
    tradition_preference = Column(String, nullable=True)
    wali_involvement_preference = Column(String, nullable=True)
    marital_status_preference = Column(String, nullable=True)
    financial_expectation_preference = Column(String, nullable=True)
    family_expectation_notes = Column(Text, nullable=True)
    deal_breakers = Column(JSON, nullable=True)
