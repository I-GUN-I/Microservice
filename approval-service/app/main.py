import threading
from app.rabbitmq import rabbitmq
import time
from fastapi import FastAPI
from app.api import api  # Import the Approval API router
from app.core.database import engine, Base

# Create the FastAPI app instance
app = FastAPI(title="Approval Service")

# Include the Order routes
app.include_router(api.router)

# Create the database tables
Base.metadata.create_all(bind=engine)

# run consume_orders()
def start_consumer():
    print("Starting RabbitMQ consumer")
    # Wait or else connection will fail
    time.sleep(10)
    rabbitmq.consume_orders()

# Run rabbit consumer in a background thread
consumer_thread = threading.Thread(target=start_consumer, daemon=True)
consumer_thread.start()