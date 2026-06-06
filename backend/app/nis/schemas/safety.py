from pydantic import BaseModel, ConfigDict
from typing import Optional

class ReportRequest(BaseModel):
    reported_user_id: str
    flag_type: str
    severity: str
    context: Optional[str] = None

class ReportResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    report_id: str
    status: str
    safety_flag_created: bool
    human_review_required: bool
    message: str
