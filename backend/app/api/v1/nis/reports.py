from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.safety import ReportRequest, ReportResponse
from app.nis.services.safety_service import NISSafetyService
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.post("", response_model=ReportResponse)
async def submit_report(req: ReportRequest, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISSafetyService.submit_report(current_user.user_id, req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
