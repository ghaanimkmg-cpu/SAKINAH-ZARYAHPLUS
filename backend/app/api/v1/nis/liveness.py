from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext
from app.nis.schemas.kyc import LivenessStartResponse, LivenessSandboxPayload, LivenessStatusResponse
from app.nis.services.kyc_service import NISKYCService

router = APIRouter()

@router.post("/start", response_model=LivenessStartResponse)
async def start_liveness(current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.start_liveness_flow(current_user.user_id)

@router.get("/status", response_model=LivenessStatusResponse)
async def get_liveness_status(current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.get_liveness_status(current_user.user_id)

@router.post("/sandbox/complete", response_model=LivenessStatusResponse)
async def liveness_sandbox_complete(payload: LivenessSandboxPayload, current_user: UserContext = Depends(get_current_user)):
    return await NISKYCService.process_liveness_sandbox(payload, current_user.user_id)
