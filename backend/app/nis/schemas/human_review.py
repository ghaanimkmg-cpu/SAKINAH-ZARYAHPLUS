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

class ReviewRecordSafe(BaseModel):
    model_config = ConfigDict(extra="ignore")
    review_id: str
    user_id: str
    severity: str
    status: str
    flag_id: str
    decision: Optional[str] = None
