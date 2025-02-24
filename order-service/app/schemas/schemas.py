from pydantic import BaseModel
from datetime import datetime
# Schemas for response
class Order(BaseModel):
    id: int
    title: str
    product: str
    amount: int
    price: float
    supplier_id: int
    supplier_name: str
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Creating
class OrderCreate(BaseModel):
    title: str
    product: str
    amount: int
    price: float

    class Config:
        from_attributes = True