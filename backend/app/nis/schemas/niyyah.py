from typing import Optional
from pydantic import BaseModel, Field

class NiyyahUpdateRequest(BaseModel):
    intention_text: Optional[str] = Field(None, description="The user's Niyyah intention text")

class NiyyahResponse(BaseModel):
    intention_text: Optional[str] = None
    is_complete: bool
