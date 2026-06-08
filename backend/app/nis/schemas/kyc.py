from pydantic import BaseModel, Field
from typing import Optional
from app.nis.enums.nis_enums import VerificationStatus, EligibilityStatus, Gender

class KYCStartResponse(BaseModel):
    status: str
    session_id: Optional[str] = None
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
    status: str
    verification_level: Optional[str] = None
    human_review_required: bool = False
    failure_reason: Optional[str] = None

class EligibilityResponse(BaseModel):
    eligibility_status: EligibilityStatus
    can_enter_matching: bool
    requires_human_review: bool
    message: str

class KycSandboxPayload(BaseModel):
    verified_name: str
    verified_age: int
    verified_gender: str

class LivenessSandboxPayload(BaseModel):
    liveness_status: str
    face_match_status: str

class LivenessStartResponse(BaseModel):
    status: str
    session_id: Optional[str] = None
    message: str

class LivenessStatusResponse(BaseModel):
    status: str
    liveness_status: Optional[str] = None
    face_match_status: Optional[str] = None
    human_review_required: bool = False
