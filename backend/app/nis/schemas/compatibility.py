from pydantic import BaseModel
from typing import List, Optional

class DimensionScore(BaseModel):
    dimension: str
    score: int  # 0 to 100
    notes: Optional[str] = None
    is_tension_point: bool = False
    is_dangerous_mismatch: bool = False

class CompatibilityResult(BaseModel):
    overall_score: int
    dimensions: List[DimensionScore]
    tension_points: List[str]
    dangerous_mismatches: List[str]
    is_compatible: bool
