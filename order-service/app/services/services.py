import requests
import os
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.rabbitmq import rabbitmq
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
    # Get suitable supplier from supplier-service and raise error (raise_for_status) if fail to fetch
    try:
        response = requests.get(
            SUPPLIER_SERVICE_URL,
            params={"product_name": order.product, "order_quantity": order.amount},
        )
        response.raise_for_status()
        best_supplier = response.json()
    # Raise error if API can't find a suitable supplier
    except requests.exceptions.RequestException:
        raise ValueError(f"No suitable supplier was found.")

    # Create the Order model with object OrderCreate data and suitable supplier details from the API response
    db_order = models.Orders(
        **order.model_dump(),
        supplier_id=best_supplier["id"],
        supplier_name=best_supplier["name"]
    )
    
    # Add order then refresh database
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Publish db_order data to rabbitMQ
    rabbitmq.publish_order({
        "order_id": db_order.id,
        "order_title": db_order.title,
        "order_product": db_order.product,
        "order_amount": db_order.amount,
        "order_price": db_order.price,
        "supplier_name": db_order.supplier_name
    })

    return db_order