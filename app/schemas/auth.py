from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal
from datetime import datetime


# -----------------------------
# User Registration Schema
# -----------------------------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    role: Literal["Admin", "Warehouse Manager"]


# -----------------------------
# User Login Schema
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# User Response Schema
# -----------------------------
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# JWT Token Response Schema
# -----------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# -----------------------------
# Token Payload Schema
# -----------------------------
class TokenData(BaseModel):
    user_id: int
    role: str