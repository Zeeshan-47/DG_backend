# app/routers/users.py
from fastapi import APIRouter, Depends
from app.core.security import get_current_user # Adjust import path to where your get_current_user is
from app.models.user import User
from app.schemas.auth_schema import UserResponse
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Schema for updates
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

@router.put("/users/me", response_model=UserResponse)
async def update_me(update_data: UserUpdate, current_user: User = Depends(get_current_user)):
    # Update fields if provided
    if update_data.full_name:
        current_user.full_name = update_data.full_name
    if update_data.address:
        current_user.address = update_data.address
    if update_data.phone:
        current_user.phone = update_data.phone
        
    await current_user.save()
    return current_user

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user