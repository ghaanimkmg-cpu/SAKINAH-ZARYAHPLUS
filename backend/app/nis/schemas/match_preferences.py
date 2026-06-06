from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List
from typing_extensions import Self

class MatchPreferences(BaseModel):
    age_range_min: int = Field(..., ge=18, le=100)
    age_range_max: int = Field(..., ge=18, le=100)
    location_preference: str
    relocation_openness: str
    nikah_timeline: str
    tradition_preference: str
    wali_involvement_preference: str
    marital_status_preference: str
    financial_expectation_preference: str
    family_expectation_notes: Optional[str] = None
    deal_breakers: List[str] = []

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode='after')
    def check_age_range(self) -> Self:
        if self.age_range_min > self.age_range_max:
            raise ValueError("age_range_min cannot be greater than age_range_max")
        return self
