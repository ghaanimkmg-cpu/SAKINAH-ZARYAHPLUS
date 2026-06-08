from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.mirror import MirrorUpdateRequest, MirrorResponse
from app.nis.services.mirror_service import NISMirrorService
import uuid

router = APIRouter()

@router.get("/me", response_model=MirrorResponse)
def get_mirror(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISMirrorService.get_my_mirror(db, uid)

@router.put("/me", response_model=MirrorResponse)
def update_mirror(
    request: MirrorUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISMirrorService.update_my_mirror(db, uid, request)
