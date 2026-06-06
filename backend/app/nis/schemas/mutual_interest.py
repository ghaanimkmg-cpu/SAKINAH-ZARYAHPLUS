from pydantic import BaseModel

class InterestActionResponse(BaseModel):
    status: str
    mutual_interest: bool
    message: str
