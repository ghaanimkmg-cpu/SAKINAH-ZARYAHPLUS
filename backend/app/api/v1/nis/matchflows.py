from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.nis.schemas.matchflow import MatchflowResponse, DecisionRequest, DecisionResponse
from app.nis.services.matchflow_service import NISMatchflowService
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("/{matchflow_id}", response_model=MatchflowResponse)
def get_matchflow(matchflow_id: str, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISMatchflowService.get_matchflow(db, matchflow_id, current_user.user_id)
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{matchflow_id}/decision", response_model=DecisionResponse)
def submit_decision(matchflow_id: str, req: DecisionRequest, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    # Minimal safe mock logic as requested by user
    if req.outcome not in ["PROCEED", "PAUSE", "CLOSE"]:
        raise HTTPException(status_code=400, detail="Invalid outcome")
    return DecisionResponse(status="DECISION_RECORDED", matchflow_id=matchflow_id, outcome=req.outcome)
