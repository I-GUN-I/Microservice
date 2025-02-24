import requests
import os
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from dotenv import load_dotenv
# Get SUPPLIER_SERVICE_URL for .env file
load_dotenv()
SUPPLIER_SERVICE_URL = os.getenv("SUPPLIER_SERVICE_URL")

def get_order(db: Session, order_id: int):
    """Retrieve an order by ID."""
    return db.query(models.Orders).filter(models.Orders.id == order_id).first()

def get_all_orders(db: Session):
    """Retrieve all orders by most recently created."""
    return db.query(models.Orders).order_by(models.Orders.created_at.desc()).all()

def create_order(db: Session, order: schemas.OrderCreate):
    """Create a new order and assign a suitable supplier using an external API."""
    # Get suitable supplier data and raise error if fail to fetch data
    try:
        response = requests.get(
            SUPPLIER_SERVICE_URL,
            params={"product_name": order.product, "order_quantity": order.amount},
        )
        response.raise_for_status()
        best_supplier = response.json()
    # Raise error if API can't find a suitable supplier
    except requests.exceptions.RequestException as e:
        raise ValueError(f"No suitable supplier was found.")

    # Create the order model with supplier details from the API response
    db_order = models.Orders(
        **order.model_dump(),
        supplier_id=best_supplier["id"],
        supplier_name=best_supplier["name"]
    )
    # Add order then refresh databease and return to be use as response
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order