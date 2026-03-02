from pydantic import BaseModel, Field, EmailStr


class AuthUserS(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
