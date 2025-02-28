from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.services import services

router = APIRouter()

@router.get("/approvals", response_model=List[schemas.Approval])
def get_all_approvals(db: Session = Depends(get_db)):
    """Get all approvals."""
    approval = services.get_all_approvals(db)
    return approval

@router.get("/approvals/{approval_id}", response_model=schemas.Approval)
def get_approval(approval_id: int, db: Session = Depends(get_db)):
    """Get an order by ID."""
    approval = services.get_approval_by_id(db, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail=f"Approval ID '{approval_id}' not found")
    return approval

@router.get("/approvals/orders/{order_id}", response_model=schemas.Approval)
def get_approval_by_order_id(order_id: int, db: Session = Depends(get_db)):
    """Retrieve an approval by order's ID."""
    approval = services.get_approval_by_order_id(db, order_id)
    if not approval:
        raise HTTPException(status_code=404, detail=f"Approval with Order ID '{order_id}' not found")
    return approval

@router.put("/approvals/{approval_id}", response_model=schemas.Approval)
def update_approval_status(approval_id: int, approval_update: schemas.ApprovalUpdate,db: Session = Depends(get_db)):
    """Update the status of an approval. The status are PENDING APPROVED and REJECTED"""
    try:
        approval = services.update_approval_status(db, approval_id, approval_update)
        return approval
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
