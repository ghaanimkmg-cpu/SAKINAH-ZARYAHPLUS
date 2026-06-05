from sqlalchemy import Column, String, Enum as SQLEnum, ForeignKey, Integer, Boolean, Float, Text, JSON
from app.nis.models.base import NISBaseModel
from app.nis.enums.nis_enums import EligibilityStatus

class NISUser(NISBaseModel):
    __tablename__ = "nis_users"
    zaryah_user_id = Column(String, unique=True, index=True, nullable=False)
    eligibility_status = Column(SQLEnum(EligibilityStatus), default=EligibilityStatus.NEEDS_REVIEW)
