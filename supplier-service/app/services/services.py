from sqlalchemy.orm import Session
from app.models import models
from sqlalchemy import func
from app.schemas import schemas
# db is Session of currently connected database
def get_all_suppliers(db: Session):
    """Retrieve all suppliers."""
    return db.query(models.Supplier).all()

def get_supplier(db: Session, supplier_id: int):
    """Retrieve a supplier by ID."""
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()

def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    """Create a new supplier."""
    # Check if a supplier with the same name already exists
    exist_supplier = db.query(models.Supplier).filter(func.lower(models.Supplier.name) == func.lower(supplier.name)).first()
    if exist_supplier:
        raise ValueError(f"Supplier '{supplier.name}' already exists.")

    # Model to a dictionary for converting product names to lowercase
    supplier_data = supplier.model_dump()
    if "products" in supplier_data and supplier_data["products"]:
        supplier_data["products"] = [p.lower() for p in supplier_data["products"]]
    
    # Back to Model
    db_supplier = models.Supplier(**supplier_data)

    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, supplier_id: int, supplier_update: schemas.SupplierUpdate):
    """Update an existing supplier."""
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    # Raise error if not found
    if not db_supplier:
        raise ValueError(f"Supplier ID '{supplier_id}' not found.")

    # Check if the supplier name is being changed and if the new name already exists
    if supplier_update.name:
        exist_supplier = db.query(models.Supplier).filter(func.lower(models.Supplier.name) == func.lower(supplier_update.name)).first()
        if exist_supplier and exist_supplier.id != supplier_id:
            raise ValueError(f"Supplier '{supplier_update.name}' already exists.")

    # Exclude any fields that were not set 
    update_data = supplier_update.model_dump(exclude_unset=True)

    # Convert product names to lowercase before updating
    if "products" in update_data and update_data["products"]:
        update_data["products"] = [p.lower() for p in update_data["products"]]
        
    # Set atr in update_data
    for key, value in update_data.items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    """Delete a supplier by ID."""
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not db_supplier:
        raise ValueError(f"Supplier ID '{supplier_id}' not found.")

    db.delete(db_supplier)
    db.commit()


def find_best_supplier(db: Session, product_name: str, order_quantity: int):
    """Find the best supplier based on case-insensitive product name search and order quantity."""
    return (
        db.query(models.Supplier)
        .filter(
            func.lower(product_name) == func.any_(models.Supplier.products),  # Case-insensitive product match
            models.Supplier.min_order <= order_quantity,  # Ensure minimum order quantity is met
            models.Supplier.max_order >= order_quantity   # Ensure maximum order quantity is not exceeded
        )
        .order_by(models.Supplier.rating.desc())  # Prioritize by rating
        .first()
    )