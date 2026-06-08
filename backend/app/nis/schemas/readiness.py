from pydantic import BaseModel

class ReadinessHomeResponse(BaseModel):
    niyyah_complete: bool
    values_complete: bool
    mirror_complete: bool
    portrait_complete: bool
    demographics_complete: bool
    is_fully_ready: bool
