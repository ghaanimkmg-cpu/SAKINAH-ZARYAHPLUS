from pydantic import BaseModel
from typing import List, Optional

class DimensionScore(BaseModel):
    dimension: str
    status: str  # STRONG, MODERATE, WEAK, INCOMPATIBLE
    notes: Optional[str] = None
    is_tension_point: bool = False
    is_dangerous_mismatch: bool = False
    is_shared_strength: bool = False

class CompatibilityResult(BaseModel):
    compatibility_status: str
    confidence_level: str
    dimension_results: List[DimensionScore]
    shared_strengths: List[str]
    possible_tension_points: List[str]
    dangerous_mismatches: List[str]
    reasoning_summary: str
    review_required: bool
