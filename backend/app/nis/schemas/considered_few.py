from pydantic import BaseModel
from typing import List

class ConsideredCandidate(BaseModel):
    candidate_user_id: str
    display_type: str = "CHARACTER_PORTRAIT"
    photo_visible: bool = False
    confidence_level: str
    shared_strengths: List[str]
    possible_tension_points: List[str]
    honest_edge: str
    raya_preview: str

class ConsideredFewResponse(BaseModel):
    status: str
    candidates: List[ConsideredCandidate] = []
    message: str
