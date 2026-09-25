from beanie import Document
from pydantic import BaseModel

class Deal(Document):
    title: str          # e.g., "Deal 1"
    price: float        # e.g., 480.0
    description: str    # e.g., "500g Chicken pulao..."
    image_url: str

    class Settings:
        name = "deals"