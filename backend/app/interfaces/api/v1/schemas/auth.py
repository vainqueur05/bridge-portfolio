"""Schémas pour l'authentification."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nom: str = Field(..., min_length=2, max_length=150)
    role: str = Field(default="observateur")


class UserResponse(BaseModel):
    id: int
    email: str
    nom: Optional[str]
    role: str
    actif: bool
    created_at: str
    model_config = {"from_attributes": True}