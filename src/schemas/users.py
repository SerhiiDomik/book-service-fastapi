from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from src.database.models.users import RoleEnum

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    group_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
