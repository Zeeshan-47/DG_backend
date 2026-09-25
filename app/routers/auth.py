from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import random
import string
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token # Assuming you have these
from app.core.email import send_otp_email
from pydantic import BaseModel, EmailStr

router = APIRouter()

# --- SCHEMAS ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    address: str
    phone: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class ResetPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

# --- HELPER ---
def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

# --- ROUTES ---

@router.post("/signup", status_code=201)
async def signup(user_input: UserCreate):
    existing_user = await User.find_one(User.email == user_input.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    otp = generate_otp()
    
    # Create User (Verified=False)
    new_user = User(
        email=user_input.email,
        hashed_password=get_password_hash(user_input.password),
        full_name=user_input.full_name,
        address=user_input.address,
        phone=user_input.phone,
        is_verified=False,
        otp=otp
    )
    await new_user.create()
    
    # Send Email
    await send_otp_email(user_input.email, otp)
    
    return {"message": "Account created. Check email for OTP."}

@router.post("/verify-email")
async def verify_email(data: VerifyOTP):
    user = await User.find_one(User.email == data.email)
    if not user or user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user.is_verified = True
    user.otp = None # Clear OTP
    await user.save()
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
async def forgot_password(email: str):
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    otp = generate_otp()
    user.otp = otp
    await user.save()
    
    await send_otp_email(email, otp)
    return {"message": "OTP sent to your email"}

@router.post("/reset-password")
async def reset_password(data: ResetPassword):
    user = await User.find_one(User.email == data.email)
    if not user or user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user.hashed_password = get_password_hash(data.new_password)
    user.otp = None
    await user.save()
    
    return {"message": "Password updated successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Please verify your email first")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}