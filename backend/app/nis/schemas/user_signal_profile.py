from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserSignalProfile(BaseModel):
    # Core 13 Dimensions
    emotional_steadiness: str
    anger_intensity: str = "MODERATE"
    conflict_repair_style: str
    communication_style: str
    attachment_needs: str = "SECURE"
    ego_humility: str = "BALANCED"
    family_responsibility: str
    financial_responsibility: str = "BALANCED"
    financial_expectation: str
    marriage_readiness: str
    social_lifestyle: str
    deen_alignment: str
    boundary_respect: str = "RESPECTFUL"
    stability_risk: str = "LOW"
    
    # Legacy / Other fields
    wali_comfort: str
    life_direction: str
    self_awareness_level: str
    safety_risk_level: str = "LOW"
    confidence_level: str = "HIGH"
    missing_signal_areas: List[str] = []
    review_required: bool = False

    model_config = ConfigDict(extra="ignore")
