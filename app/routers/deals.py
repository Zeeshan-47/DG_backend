from fastapi import APIRouter, HTTPException
from typing import List
from app.models.deal import Deal

router = APIRouter()

# Get All Deals (For User)
@router.get("/", response_model=List[Deal])
async def get_deals():
    return await Deal.find_all().to_list()

# Add Deal (For Admin)
@router.post("/", response_model=Deal)
async def create_deal(deal: Deal):
    await deal.create()
    return deal

@router.delete("/{item_id}")
async def delete_deals(item_id: str):

    item = await Deal.get(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await item.delete()
    return {"message": "Item deleted successfully"}