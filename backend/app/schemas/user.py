"""
Pydantic schemas for User model validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base User schema
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None

# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for password update
class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

# Schema for user response (excludes sensitive data)
class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    full_name: str

    class Config:
        from_attributes = True

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None