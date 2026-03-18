from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Literal["admin", "gestor", "rh", "visualizador"]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
