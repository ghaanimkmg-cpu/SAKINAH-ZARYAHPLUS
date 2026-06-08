from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.kyc import KYCStartResponse, KYCStatusResponse, KycSandboxPayload
from app.nis.services.kyc_service import NISKYCService

router = APIRouter()

@router.post("/start", response_model=KYCStartResponse)
async def start_kyc(current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.start_kyc_flow(current_user.user_id)

@router.get("/status", response_model=KYCStatusResponse)
async def get_kyc_status(current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.get_kyc_status(current_user.user_id)

@router.post("/sandbox/complete", response_model=KYCStatusResponse)
async def kyc_sandbox_complete(payload: KycSandboxPayload, current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.process_kyc_sandbox(payload, current_user.user_id)
