from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class RayaExplanationResult(BaseModel):
    title: str
    preview: str
    explanation: str
    tone: str
    decision_boundary: str

class RayaScriptInputs(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    shared_strengths: List[str] = []
    possible_tension_points: List[str] = []
    compatibility_status: Optional[str] = None
    confidence_level: Optional[str] = None
    final_status: Optional[str] = None
    review_required: bool = False
    no_match_status: bool = False
