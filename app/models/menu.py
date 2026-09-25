from beanie import Document
from pydantic import BaseModel
from typing import List, Optional

# 1. Create a Schema for Variations
class Variation(BaseModel):
    name: str   # e.g., "Single Serving" or "1kg"
    price: float

# 2. Update the Main Model
class MenuItem(Document):
    name: str
    description: str
    price: float       # Base price
    image_url: str
    category: str
    is_available: bool = True
    variations: List[Variation] = [] # <--- NEW FIELD

    class Settings:
        name = "menu_items"