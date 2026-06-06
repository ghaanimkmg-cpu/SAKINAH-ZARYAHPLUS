from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserSignalProfile(BaseModel):
    emotional_steadiness: str
    communication_style: str
    conflict_repair_style: str
    family_responsibility: str
    deen_alignment: str
    marriage_readiness: str
    financial_expectation: str
    wali_comfort: str
    life_direction: str
    self_awareness_level: str
    social_lifestyle: str
    safety_risk_level: str = "LOW"
    confidence_level: str = "HIGH"
    missing_signal_areas: List[str] = []
    review_required: bool = False

    model_config = ConfigDict(extra="ignore")
