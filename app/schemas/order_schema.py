from pydantic import BaseModel
from typing import List, Optional as optional

class OrderItemSchema(BaseModel):
    menu_item_id: str
    name: str
    quantity: int
    price: float
    instructions: optional[str] = None

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]
    total_amount: float
    delivery_address: str
    payment_method: str