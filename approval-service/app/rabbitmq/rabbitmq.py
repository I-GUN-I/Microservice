import pika
import json
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import models
from dotenv import load_dotenv

# Load RABBITMQ_URL
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

def save_order(order_data):
    """Save received order data to the Approval database."""
    # Connect to Approval database
    db: Session = SessionLocal()
    try:
        # Save data from order_data to approval model object
        approval = models.Approval(
            order_id=order_data["order_id"],
            order_title=order_data["order_title"],
            order_product=order_data["order_product"],
            order_amount=order_data["order_amount"],
            order_price=order_data["order_price"],
            order_supplier=order_data["supplier_name"]
        )
        # Add approval to db
        db.add(approval)
        db.commit()
        print(f"Order save in Approval ID '{approval.id}'")
    # If error rollback the db
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    # Close connection to db after saved
    finally:
        db.close()

def callback(ch, method, properties, body):
    """Callback function to process messages from RabbitMQ."""
    try:
        # Load data from message that got consumed
        order_data = json.loads(body)
        print(f"Received order: {order_data}")

        # Using func save_order to save order to DB
        save_order(order_data)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")

def consume_orders():
    """Consume messages from the order_approval queue."""
    params = pika.URLParameters(RABBITMQ_URL) 
    connection = pika.BlockingConnection(params) 
    channel = connection.channel() # Connect to rabbit

    channel.queue_declare(queue="order_approval", durable=True) # Queue declaration 

    channel.basic_consume(queue="order_approval", on_message_callback=callback) # Connect to Queue order_approval

    print("Approval Service is waiting for orders...")
    # Start consuming
    channel.start_consuming()
