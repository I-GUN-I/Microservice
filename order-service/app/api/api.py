from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.services import services

router = APIRouter()

@router.get("/orders", response_model=List[schemas.Order])
def get_all_orders(db: Session = Depends(get_db)):
    """Get all orders."""
    orders = services.get_all_orders(db)
    return orders

@router.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get an order by ID."""
    order = services.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order ID '{order_id}' not found")
    return order

@router.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create a new order with a suitable supplier."""
    try:
        order_created = services.create_order(db, order)
        return order_created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))