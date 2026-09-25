from fastapi import APIRouter, HTTPException
from app.models.menu import MenuItem
from typing import List

router = APIRouter()

@router.get("/", response_model=List[MenuItem])
async def get_menu():
    return await MenuItem.find(MenuItem.is_available == True).to_list()

@router.post("/", response_model=MenuItem)
async def add_menu_item(item: MenuItem):
    # In a real app, restrict this to Admin users
    await item.create()
    return item

@router.delete("/{item_id}")
async def delete_menu_item(item_id: str):
    
    item = await MenuItem.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await item.delete()
    return {"message": "Item deleted successfully"}