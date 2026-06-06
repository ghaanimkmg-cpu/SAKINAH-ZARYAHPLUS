from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.kyc import KYCStartResponse, KYCCallbackPayload, KYCStatusResponse
from app.nis.services.kyc_service import NISKYCService

router = APIRouter()

@router.post("/start", response_model=KYCStartResponse)
async def start_kyc(current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.start_kyc_flow(current_user.user_id)

@router.post("/callback", response_model=KYCStatusResponse)
async def kyc_callback(payload: KYCCallbackPayload, current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.process_callback(payload, current_user.user_id)
