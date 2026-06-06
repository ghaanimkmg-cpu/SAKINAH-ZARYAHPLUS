from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.user_signal_profile import UserSignalProfile
from app.nis.services.user_signal_profile_service import NISUserSignalProfileService

router = APIRouter()

@router.get("/me", response_model=UserSignalProfile)
async def get_my_profile(current_user: UserContext = Depends(get_current_user)):
    return await NISUserSignalProfileService.get_profile(current_user.user_id)

@router.put("/me", response_model=UserSignalProfile)
async def update_my_profile(profile: UserSignalProfile, current_user: UserContext = Depends(get_current_user)):
    return await NISUserSignalProfileService.update_profile(current_user.user_id, profile)
