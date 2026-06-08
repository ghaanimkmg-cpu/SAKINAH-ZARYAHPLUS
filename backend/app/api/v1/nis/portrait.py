from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.portrait import PortraitUpdateRequest, PortraitResponse
from app.nis.services.portrait_service import NISPortraitService
import uuid

router = APIRouter()

@router.get("/me", response_model=PortraitResponse)
def get_portrait(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISPortraitService.get_my_portrait(db, uid)

@router.put("/me", response_model=PortraitResponse)
def update_portrait(
    request: PortraitUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISPortraitService.update_my_portrait(db, uid, request)
