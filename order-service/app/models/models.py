from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

# Base class for ORM
class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True) # ID of Orders
    title = Column(String, nullable=False) # Title of order
    product = Column(String, nullable=False)  # Name of the ordered product
    amount = Column(Integer, nullable=False)  # Total quantity
    price = Column(Float, nullable=False)  # Total price
    created_at = Column(DateTime, server_default=func.now())  # Use DB to calculate the timestamp
    supplier_id = Column(Integer, nullable=False)  # Supplier ID as an integer
    supplier_name = Column(String, nullable=False)  # Supplier name, stored as a string