from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.nis.schemas.auth import UserContext

router = APIRouter()

@router.get("/me", response_model=UserContext)
async def get_current_user_info(current_user: UserContext = Depends(get_current_user)):
    """
    Test endpoint to verify user context dependency.
    """
    return current_user
