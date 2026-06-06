from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.nis.schemas.mutual_interest import InterestActionResponse
from app.nis.services.mutual_interest_service import NISMutualInterestService
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.post("/candidates/{candidate_id}/interest", response_model=InterestActionResponse)
def express_interest(candidate_id: str, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISMutualInterestService.record_interest(db, current_user.user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/candidates/{candidate_id}/pass", response_model=InterestActionResponse)
def express_pass(candidate_id: str, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISMutualInterestService.record_pass(db, current_user.user_id, candidate_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

from app.nis.schemas.mutual_interest import CandidateDetailResponse

@router.get("/candidates/{candidate_id}", response_model=CandidateDetailResponse)
async def get_candidate_detail(candidate_id: str, current_user: UserContext = Depends(get_current_user)):
    # Minimal safe mock logic as requested by user
    return CandidateDetailResponse(
        candidate_id=candidate_id,
        display_name="Candidate",
        age=28,
        location="Mock City",
        profession="Professional",
        sect="Sunni",
        prayer_frequency="Always",
        shared_strengths=["Family-oriented", "Prays regularly"],
        honest_edge="Open to relocating"
    )
