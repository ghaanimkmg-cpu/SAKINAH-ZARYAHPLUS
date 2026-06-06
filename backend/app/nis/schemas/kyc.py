from pydantic import BaseModel, Field
from typing import Optional
from app.nis.enums.nis_enums import VerificationStatus, EligibilityStatus, Gender

class KYCStartResponse(BaseModel):
    status: str
    provider: str
    message: str

class KYCCallbackPayload(BaseModel):
    provider_reference: str
    verified_name: str
    age: int
    gender: Gender
    identity_hash: str
    liveness_score: float = Field(..., ge=0, le=1)
    face_match_score: float = Field(..., ge=0, le=1)
    verification_passed: bool

class KYCStatusResponse(BaseModel):
    verification_status: VerificationStatus
    human_review_required: bool
    review_reason: Optional[str] = None
    message: str

class EligibilityResponse(BaseModel):
    eligibility_status: EligibilityStatus
    can_enter_matching: bool
    requires_human_review: bool
    message: str
