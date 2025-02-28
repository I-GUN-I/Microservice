from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.services import services

# Create an instance of APIRouter then define routes
router = APIRouter()

# Response_model is the return response format, in this case it a List of Supplier objects
@router.get("/suppliers/", response_model=List[schemas.Supplier])

# Inject the Session (db) created by get_db() into the function
def get_all_suppliers(db: Session = Depends(get_db)):
    """Retrieve all suppliers."""
    return services.get_all_suppliers(db)

@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)  
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Retrieve a supplier by ID."""
    db_supplier = services.get_supplier(db, supplier_id)
    # If get_supplier return empty raise error
    if db_supplier is None:
        raise HTTPException(status_code=404, detail=f"Supplier '{supplier_id}' not found")
    return db_supplier

@router.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    """Create a new supplier."""
    try:
        # Create the supplier
        return services.create_supplier(db=db, supplier=supplier)
    except ValueError as e:
        # Raise an Error if supplier already exists
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(supplier_id: int, supplier: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    """Update an existing supplier."""
    try:
        # Update the supplier
        db_supplier = services.update_supplier(db=db, supplier_id=supplier_id, supplier_update=supplier)
        return db_supplier
    except ValueError as e:
        # Raise an Error if can't find the supplier
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/suppliers/{supplier_id}", response_model=None)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Delete a supplier by ID."""
    try:
        services.delete_supplier(db, supplier_id)
        # Return a success message with the supplier's ID
        return {"message": f"Supplier ID '{supplier_id}' has been successfully deleted."}
    except ValueError as e:
        # Raise an Error if supplier don't exists
        raise HTTPException(status_code=400, detail=str(e))

    
@router.get("/best-supplier", response_model=schemas.Supplier)
def get_best_supplier(product_name: str, order_quantity: int, db: Session = Depends(get_db)):
    """Find the best supplier based on product and order quantity."""
    db_supplier = services.find_best_supplier(db, product_name, order_quantity)
    # If find_best_supplier return empty raise error
    if not db_supplier:
        raise HTTPException(status_code=404, detail="No suitable supplier was found")
    return db_supplier