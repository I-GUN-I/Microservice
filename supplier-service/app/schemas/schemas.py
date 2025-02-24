from pydantic import BaseModel
from typing import List, Optional
# Schemas for response
class Supplier(BaseModel):
    id: int
    name: str
    contact_phone: str
    contact_email: str
    address: str
    rating: int
    products: List[str]
    min_order: int
    max_order: int
    # For using with ORM
    class Config:
        from_attributes = True

# Schemas for Creating
class SupplierCreate(BaseModel):
    name: str
    contact_phone: str
    contact_email: str
    address: Optional[str] = None  # Address is optional
    rating: Optional[int] = 0  # Optional with Default rating of 0
    products: Optional[List[str]] = []  # Default empty list of products
    min_order: Optional[int] = 1  # Optional with Default minimum order of 1
    max_order: Optional[int] = 999  # Optional with Default maximum order of 99

    class Config:
        from_attributes = True

# Schemas for Updating
class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    rating: Optional[int] = None
    products: Optional[List[str]] = None
    min_order: Optional[int] = None
    max_order: Optional[int] = None

    class Config:
        from_attributes = True