from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.human_review import ReviewDecisionRequest, ReviewDecisionResponse
from app.nis.services.human_review_service import NISHumanReviewService
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.post("/{review_id}/decision", response_model=ReviewDecisionResponse)
async def submit_review_decision(review_id: str, req: ReviewDecisionRequest, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISHumanReviewService.submit_decision(review_id, req, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
