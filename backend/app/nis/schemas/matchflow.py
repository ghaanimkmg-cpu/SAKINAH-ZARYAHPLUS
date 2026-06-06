from pydantic import BaseModel, ConfigDict
from typing import List

class MatchflowStep(BaseModel):
    step: str
    status: str

class MatchflowResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    matchflow_id: str
    current_step: str
    steps: List[MatchflowStep]
    chat_open: bool
    message: str

class DecisionRequest(BaseModel):
    outcome: str

class DecisionResponse(BaseModel):
    status: str
    matchflow_id: str
    outcome: str
