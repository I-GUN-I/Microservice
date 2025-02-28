from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

# Base class for ORM
class Approval(Base):
    __tablename__ = 'Approvals'

    id = Column(Integer, primary_key=True, index=True) # ID of Approval
    order_id = Column(Integer, nullable=False) # ID of received order
    order_title = Column(String, nullable=False) # Title of received order
    order_product = Column(String, nullable=False)  # Product which was ordered
    order_amount = Column(Integer, nullable=False)  # Quantity of the order
    order_price = Column(Float, nullable=False)  # Total price of the order
    order_supplier = Column(String, nullable=False)  # Name of order's Supplier
    order_status = Column(String, nullable=False, default="PENDING") # Status of order, default is pending
    order_receive = Column(DateTime, server_default=func.now()) # Date of when Approval got the order
    approval_date = Column(DateTime, onupdate=func.now(), nullable=True) # Will be set when Status change, can be null