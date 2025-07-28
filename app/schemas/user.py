from typing import Optional

from fastapi.openapi.models import EmailStr
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = {
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    user_id: Optional[int]
    role: Optional[str]
    session_uuid: Optional[str]
    exp: Optional[int]
    token_type: str = "bearer"