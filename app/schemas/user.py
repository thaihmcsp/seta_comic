from typing import Optional
from fastapi import UploadFile, File, Form
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
    model_config = {"from_attributes": True}


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

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdateUserRequest(BaseModel):
    username: Optional[str] = Form(..., description="Username"),
    email: Optional[EmailStr] = Form(..., description="Email"),
    avatar: UploadFile = File(..., description="Avatar image file"),