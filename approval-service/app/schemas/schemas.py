from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema for responses
class Approval(BaseModel):
    id: int
    order_title: str
    order_id: int
    order_product: str
    order_amount: int
    order_price: float
    order_supplier: str
    order_status: str = "PENDING"
    order_receive: datetime
    approval_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApprovalUpdate(BaseModel):
    order_status: str

    class Config:
        from_attributes = True
