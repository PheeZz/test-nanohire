from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from datetime import datetime


class AuthUserS(BaseModel):
    """Схема для логина"""
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterUserS(BaseModel):
    """Схема для регистрации"""
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = Field(None, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    hh_manager_id: str = Field(max_length=255)


class UserResponseS(BaseModel):
    """Схема данных пользователя в ответе"""
    id: UUID
    email: str
    first_name: str
    middle_name: str | None
    last_name: str
    hh_manager_id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenPairS(BaseModel):
    """Схема пары токенов"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponseS(BaseModel):
    """Схема ответа при аутентификации"""
    user: UserResponseS
    tokens: TokenPairS
