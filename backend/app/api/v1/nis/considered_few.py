from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.nis.services.considered_few_service import NISConsideredFewService
from app.nis.schemas.considered_few import ConsideredFewResponse
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("", response_model=ConsideredFewResponse)
def get_considered_few(current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return NISConsideredFewService.get_considered_few(db, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
