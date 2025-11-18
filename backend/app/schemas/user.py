from pydantic import BaseModel, EmailStr, Field  # <-- Import Field
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    # --- Update this line ---
    password: str = Field(..., min_length=8, max_length=72)
    # --- End update ---

# Properties to return to client
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True