from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.nis.schemas.safety import ReportRequest, ReportResponse
from app.nis.services.safety_service import NISSafetyService
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.post("", response_model=ReportResponse)
def submit_report(req: ReportRequest, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISSafetyService.submit_report(db, current_user.user_id, req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
