from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class PortraitUpdateRequest(BaseModel):
    portrait_data: Dict[str, Any] = Field(default_factory=dict, description="JSON representing user's private holistic portrait")

class PortraitResponse(BaseModel):
    portrait_data: Dict[str, Any]
    is_complete: bool
