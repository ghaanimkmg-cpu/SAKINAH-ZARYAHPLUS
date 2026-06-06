from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.mutual_interest import InterestActionResponse
from app.nis.services.mutual_interest_service import NISMutualInterestService
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.post("/candidates/{candidate_id}/interest", response_model=InterestActionResponse)
async def express_interest(candidate_id: str, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISMutualInterestService.record_interest(current_user.user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/candidates/{candidate_id}/pass", response_model=InterestActionResponse)
async def express_pass(candidate_id: str, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISMutualInterestService.record_pass(current_user.user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
