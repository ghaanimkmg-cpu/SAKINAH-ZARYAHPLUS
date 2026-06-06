from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.nis.schemas.human_review import ReviewDecisionRequest, ReviewDecisionResponse, ReviewRecordSafe
from app.nis.services.human_review_service import NISHumanReviewService
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("", response_model=List[ReviewRecordSafe])
def list_admin_reviews(current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    return NISHumanReviewService.list_reviews(db)

@router.post("/{review_id}/decision", response_model=ReviewDecisionResponse)
def submit_review_decision(review_id: str, req: ReviewDecisionRequest, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISHumanReviewService.submit_decision(db, review_id, req, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
