from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class MirrorUpdateRequest(BaseModel):
    reflection_data: Dict[str, Any] = Field(default_factory=dict, description="JSON representing user's private reflections")

class MirrorResponse(BaseModel):
    reflection_data: Dict[str, Any]
    is_complete: bool
