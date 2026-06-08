from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.values import ValuesUpdateRequest, ValuesResponse
from app.nis.services.values_service import NISValuesService
import uuid

router = APIRouter()

@router.get("/me", response_model=ValuesResponse)
def get_values(
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISValuesService.get_my_values(db, uid)

@router.put("/me", response_model=ValuesResponse)
def update_values(
    request: ValuesUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    uid = uuid.UUID(current_user.user_id)
    return NISValuesService.update_my_values(db, uid, request)
