from fastapi import FastAPI
from app.api import api  # Import the Order API router
from app.core.database import engine, Base

# Create the FastAPI app instance
app = FastAPI(title="Order Service")

# Include the Order routes
app.include_router(api.router)

# Create the database tables
Base.metadata.create_all(bind=engine)