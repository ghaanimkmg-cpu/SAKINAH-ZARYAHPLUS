from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.niyyah import NiyyahUpdateRequest, NiyyahResponse
from app.nis.services.niyyah_service import NISNiyyahService
import uuid

router = APIRouter()

@router.get("/me", response_model=NiyyahResponse)
def get_niyyah(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISNiyyahService.get_my_niyyah(db, uid)

@router.put("/me", response_model=NiyyahResponse)
def update_niyyah(
    request: NiyyahUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISNiyyahService.update_my_niyyah(db, uid, request)
