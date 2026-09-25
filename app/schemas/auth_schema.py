from pydantic import BaseModel, EmailStr, BeforeValidator, Field
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=25)
    address: str | None = None

class UserResponse(BaseModel):
    id: PyObjectId
    email: EmailStr
    full_name: str
    role: str = "customer"
    address: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        # Allows Pydantic to read data from Beanie/ORM objects
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
