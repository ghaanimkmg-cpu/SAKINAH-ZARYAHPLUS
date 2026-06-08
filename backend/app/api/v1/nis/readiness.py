from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.readiness import ReadinessHomeResponse
from app.nis.services.readiness_service import NISReadinessService
import uuid

router = APIRouter()

@router.get("/home", response_model=ReadinessHomeResponse)
def get_readiness_home(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISReadinessService.get_readiness_home(db, uid)
