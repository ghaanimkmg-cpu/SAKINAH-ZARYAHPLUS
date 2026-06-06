from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext
from app.nis.schemas.match_preferences import MatchPreferences
from app.nis.services.match_preference_service import NISMatchPreferenceService

router = APIRouter()

@router.get("/me", response_model=MatchPreferences)
def get_my_preferences(current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    return NISMatchPreferenceService.get_preferences(db, current_user.user_id)

@router.put("/me", response_model=MatchPreferences)
def update_my_preferences(preferences: MatchPreferences, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    return NISMatchPreferenceService.update_preferences(db, current_user.user_id, preferences)
