from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.match_preferences import MatchPreferences
from app.nis.services.match_preference_service import NISMatchPreferenceService

router = APIRouter()

@router.get("/me", response_model=MatchPreferences)
async def get_my_preferences(current_user: UserContext = Depends(get_current_user)):
    return await NISMatchPreferenceService.get_preferences(current_user.user_id)

@router.put("/me", response_model=MatchPreferences)
async def update_my_preferences(preferences: MatchPreferences, current_user: UserContext = Depends(get_current_user)):
    return await NISMatchPreferenceService.update_preferences(current_user.user_id, preferences)
