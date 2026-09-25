from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from app.models.user import User
from app.models.menu import MenuItem
from app.models.order import Order
from app.routers import auth, menu, orders, users
from app.models.deal import Deal # <--- Import Model
from app.routers import deals

# Database Configuration
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = "foodies_db"

app = FastAPI(title="Foodies API")

@app.on_event("startup")
async def app_init():
    # Initialize MongoDB connection with Beanie
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[User, MenuItem, Order, Deal]
    )

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(users.router, tags=["Users"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])

@app.get("/")
async def root():
    return {"message": "Welcome to Foodies API"}
