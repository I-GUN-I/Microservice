from sqlalchemy import Column, Integer, String, ARRAY 
from app.core.database import Base

# Base class for ORM
class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True) # ID of Supplier
    name = Column(String, nullable=False, index=True) # Name of Supplier
    contact_phone = Column(String, nullable=False)  # Contact phone number
    contact_email = Column(String, nullable=False)  # Contact email address
    address = Column(String, nullable=True)  # Physical address
    rating = Column(Integer, default=0)  # Rating of the supplier (1-5 stars)
    products = Column(ARRAY(String), nullable=True)  # List of strings product names 
    min_order = Column(Integer, nullable=True, default=1)  # Minimum order quantity
    max_order = Column(Integer, nullable=True, default=999) # Maximum order quantity
