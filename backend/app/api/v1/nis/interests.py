from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.mutual_interest import InterestActionResponse
from app.nis.services.mutual_interest_service import NISMutualInterestService

router = APIRouter()

# Safe dummy dependency for tests
def get_current_user_id() -> str:
    return "user_1"

@router.post("/candidates/{candidate_id}/interest", response_model=InterestActionResponse)
async def express_interest(candidate_id: str, current_user_id: str = Depends(get_current_user_id)):
    try:
        return NISMutualInterestService.record_interest(current_user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/candidates/{candidate_id}/pass", response_model=InterestActionResponse)
async def express_pass(candidate_id: str, current_user_id: str = Depends(get_current_user_id)):
    try:
        return NISMutualInterestService.record_pass(current_user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
