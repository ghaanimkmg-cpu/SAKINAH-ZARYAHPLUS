from pydantic import BaseModel, ConfigDict
from typing import Optional

class ReviewDecisionRequest(BaseModel):
    decision: str
    notes: Optional[str] = None

class ReviewDecisionResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    review_id: str
    decision: str
    status: str
    message: str
