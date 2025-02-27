import pika
import json
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

def save_order(order_data):
    """Save received order data to the Approval database."""

    db: Session = SessionLocal()
    try:
        approval = models.Approval(
            order_title=order_data["order_title"],
            order_product=order_data["order_product"],
            order_amount=order_data["order_amount"],
            order_price=order_data["order_price"],
            order_supplier=order_data["order_supplier"]
        )
        db.add(approval)
        db.commit()
        print(f"Order saved: {approval.id}")
    except Exception as e:
        db.rollback()
        print(f"Database Error: {e}")
    finally:
        db.close()

def callback(ch, method, body):
    """Callback function to process messages from RabbitMQ."""
    try:
        order_data = json.loads(body)
        print(f"Received order: {order_data}")

        # Save order to DB
        save_order(order_data)

        # Acknowledge
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")

def consume_orders():
    """Consume messages from the order_approval queue."""
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="order_approval", durable=True)

    channel.basic_consume(queue="order_approval", on_message_callback=callback)

    print("Approval Service is waiting for orders...")
    channel.start_consuming()
