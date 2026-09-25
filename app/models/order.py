from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PREPARING = "Preparing"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

# Ensure this inherits BaseModel
class OrderItem(BaseModel):
    menu_item_id: PydanticObjectId
    name: str
    quantity: int
    price: float
    instructions: Optional[str] = None

class Order(Document):
    user_id: PydanticObjectId
    items: List[OrderItem]
    total_amount: float
    delivery_address: Optional[str] = "No Address"
    payment_method: Optional[str] = "COD"
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = datetime.now()

    class Settings:
        name = "orders"