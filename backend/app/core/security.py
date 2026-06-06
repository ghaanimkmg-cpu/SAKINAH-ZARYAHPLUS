from fastapi import Depends, HTTPException, status, Header
from app.core.config import settings
from app.nis.schemas.auth import UserContext

async def get_current_user(
    x_test_user_id: str = Header(None, alias="X-Test-User-Id")
) -> UserContext:
    """
    Dependency to get the current authenticated user.
    Firebase is NOT used as per Phase 9 rules.
    """
    if settings.APP_ENV == 'development':
        if x_test_user_id:
            return UserContext(user_id=x_test_user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated (Missing X-Test-User-Id header in dev mode)"
            )
    
    # In production, this should integrate with the real auth provider
    # Raising 501 NotImplemented for production until real auth is provided
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Production authentication integration is pending"
    )
