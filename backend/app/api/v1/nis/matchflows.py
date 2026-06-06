from fastapi import APIRouter, Depends, HTTPException
from app.nis.schemas.matchflow import MatchflowResponse
from app.nis.services.matchflow_service import NISMatchflowService
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("/{matchflow_id}", response_model=MatchflowResponse)
async def get_matchflow(matchflow_id: str, current_user: UserContext = Depends(get_current_user)):
    try:
        return NISMatchflowService.get_matchflow(matchflow_id, current_user.user_id)
    except ValueError as e:
        if "Unauthorized" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))
