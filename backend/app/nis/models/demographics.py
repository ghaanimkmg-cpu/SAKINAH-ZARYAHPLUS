from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.nis.models.base import NISBaseModel

class NISDemographicProfile(NISBaseModel):
    __tablename__ = "nis_demographic_profiles"
    user_id = Column(UUID(as_uuid=True), ForeignKey("nis_users.id"), unique=True, nullable=False)
    
    # Self-reported demographics
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    relocation_open = Column(String, nullable=True) # "OPEN", "NOT_OPEN"
    tradition = Column(String, nullable=True) # "Sunni", "Shia", "Just Muslim", etc
    marital_status = Column(String, nullable=True) # "NEVER_MARRIED", "DIVORCED", etc
    wali_preference = Column(String, nullable=True) # "REQUIRED", "PREFERRED", "NOT_REQUIRED"
    nikah_timeline = Column(String, nullable=True) # "6_MONTHS", "1_YEAR", etc

    # KYC/Verified subset
    verified_identity_name = Column(String, nullable=True)
    verified_age = Column(Integer, nullable=True)
    verified_gender = Column(String, nullable=True)
    is_kyc_verified = Column(Boolean, default=False)
    
    # We explicitly DO NOT store raw Aadhaar, government ID, or selfie photos.
