from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

# Enum for order status
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# Base schema for responses
class ApprovalBase(BaseModel):
    id: int
    order_title: str
    order_id: int
    order_product: str
    order_amount: int
    order_price: float
    order_supplier: str
    order_status: OrderStatusEnum = OrderStatusEnum.PENDING
    order_receive: datetime
    approval_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApprovalUpdate(BaseModel):
    order_status: OrderStatusEnum

    class Config:
        from_attributes = True
