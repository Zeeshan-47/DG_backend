from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional

class User(Document):
    email: EmailStr
    hashed_password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=25)
    address: str | None = None
    phone: str = Field(..., min_length=11, max_length=11)
    role: str = "customer"
    is_verified: bool = False
    otp: Optional[str] = None

    class Settings:
        name = "users"