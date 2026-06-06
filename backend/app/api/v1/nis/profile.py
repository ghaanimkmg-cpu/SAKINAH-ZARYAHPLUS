from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.nis.schemas.auth import UserContext
from app.nis.schemas.user_signal_profile import UserSignalProfile
from app.nis.services.user_signal_profile_service import NISUserSignalProfileService

router = APIRouter()

@router.get("/me", response_model=UserSignalProfile)
def get_my_profile(current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    return NISUserSignalProfileService.get_profile(db, current_user.user_id)

@router.put("/me", response_model=UserSignalProfile)
def update_my_profile(profile: UserSignalProfile, current_user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    return NISUserSignalProfileService.update_profile(db, current_user.user_id, profile)
