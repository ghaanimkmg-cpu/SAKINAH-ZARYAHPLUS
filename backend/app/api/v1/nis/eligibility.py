from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.kyc import EligibilityResponse
from app.nis.services.eligibility_service import NISEligibilityService

router = APIRouter()

@router.get("/me", response_model=EligibilityResponse)
async def get_my_eligibility(current_user: UserContext = Depends(get_current_user)):
    # Simulating DB dependency resolution with defaults for testing sandbox mode
    return await NISEligibilityService.check_eligibility(
        user_id=current_user.user_id,
        is_banned=False,
        kyc_status="VERIFIED"
    )
