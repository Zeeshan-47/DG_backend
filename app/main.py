import os
from dotenv import load_dotenv
from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.deal import Deal
from app.models.menu import MenuItem
from app.models.order import Order
from app.models.user import User
from app.routers import auth, deals, menu, orders, users

load_dotenv()

# Database Configuration
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = "foodies_db"

app = FastAPI(title="Foodies API")


@app.on_event("startup")
async def app_init():
    if not MONGO_URL:
        raise ValueError("MONGO_URL environment variable is not set!")

    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client[DB_NAME], document_models=[User, MenuItem, Order, Deal]
    )

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(users.router, tags=["Users"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])


@app.get("/")
async def root():
    return {"message": "Welcome to Foodies API"}
