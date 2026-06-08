from pydantic import BaseModel
from typing import Optional

class UserContext(BaseModel):
    user_id: str
    email: Optional[str] = None
    is_active: bool = True
    role: str = "user"
    is_admin: bool = False
    auth_source: str = "dev"
    environment: str = "development"
