from fastapi import APIRouter, HTTPException
from app.nis.services.considered_few_service import NISConsideredFewService

router = APIRouter()

@router.get("/proof-report")
async def get_proof_report():
    from app.core.config import settings
    if settings.APP_ENV != "development":
        raise HTTPException(status_code=403, detail="Forbidden. This endpoint is for development verification only.")
    return NISConsideredFewService.generate_proof_report("demo_user_ayman")
