import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

def publish_order(order_data):
    """Send order data to the approve service via RabbitMQ."""
    try:
        params = pika.URLParameters(RABBITMQ_URL) 
        connection = pika.BlockingConnection(params)
        channel = connection.channel() # Connect to rabbitmq

        channel.queue_declare(queue="order_approval", durable=True) # Create order_approval queue

        message = json.dumps(order_data) # order_data dict to json and publish it
        channel.basic_publish(
            exchange="",
            routing_key="order_approval",
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f"Order published: {message}")
        connection.close() # Close connection after published

    except Exception as e:
        print(f"Error: {e}")
