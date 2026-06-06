from pydantic import BaseModel
from typing import List

class CandidateConfidenceResult(BaseModel):
    candidate_user_id: str
    final_status: str
    confidence_level: str
    can_show_candidate: bool
    requires_human_review: bool
    reasons: List[str] = []
    blocked_reasons: List[str] = []

class NoMatchResult(BaseModel):
    status: str = "NO_SUITABLE_MATCHES_RIGHT_NOW"
    candidates: List[CandidateConfidenceResult] = []
    message: str = "We do not have someone suitable enough to show right now. We would rather wait than show the wrong person."
