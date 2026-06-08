from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ValuesUpdateRequest(BaseModel):
    values_data: Dict[str, Any] = Field(default_factory=dict, description="JSON representing user's core values mapping")

class ValuesResponse(BaseModel):
    values_data: Dict[str, Any]
    is_complete: bool
