import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.nis.schemas.auth import UserContext

security = HTTPBearer(auto_error=False)

async def get_current_user(
    x_test_user_id: str = Header(None, alias="X-Test-User-Id"),
    token: HTTPAuthorizationCredentials = Depends(security)
) -> UserContext:
    """
    Dependency to get the current authenticated user.
    In development mode, X-Test-User-Id is accepted.
    In production mode, a valid JWT Bearer token is required.
    Firebase is NOT used as per Phase 9 rules, but future devs can replace JWT decoding with Firebase Admin.
    """
    if settings.APP_ENV == 'development':
        if x_test_user_id:
            # Check if this test user is asking to be admin
            is_admin = x_test_user_id.startswith("admin_")
            return UserContext(
                user_id=x_test_user_id,
                role="admin" if is_admin else "user",
                is_admin=is_admin,
                auth_source="dev_header",
                environment="development"
            )
        # Fallthrough to token if no test header but in dev mode
    else:
        # Production mode: reject X-Test-User-Id
        if x_test_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="X-Test-User-Id not allowed in production"
            )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # Decode the generic JWT
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing 'sub'")
        role = payload.get("role", "user")
        return UserContext(
            user_id=str(user_id),
            role=role,
            is_admin=(role == "admin"),
            auth_source="jwt",
            environment=settings.APP_ENV
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_optional_current_user(
    x_test_user_id: str = Header(None, alias="X-Test-User-Id"),
    token: HTTPAuthorizationCredentials = Depends(security)
) -> UserContext | None:
    try:
        return await get_current_user(x_test_user_id, token)
    except HTTPException:
        return None

async def require_admin_user(
    current_user: UserContext = Depends(get_current_user)
) -> UserContext:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
