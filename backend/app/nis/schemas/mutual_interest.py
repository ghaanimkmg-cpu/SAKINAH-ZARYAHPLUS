from pydantic import BaseModel

class InterestActionResponse(BaseModel):
    status: str
    mutual_interest: bool
    message: str

from typing import List

class CandidateDetailResponse(BaseModel):
    candidate_id: str
    display_name: str
    age: int
    location: str
    profession: str
    sect: str
    prayer_frequency: str
    shared_strengths: List[str]
    honest_edge: str
