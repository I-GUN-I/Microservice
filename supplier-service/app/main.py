from fastapi import FastAPI
from app.api import api  # Import the supplier API router
from app.core.database import engine, Base

# Create the FastAPI app instance
app = FastAPI(title="Supplier Service")

# Include the supplier routes
app.include_router(api.router)

# Create the database tables
Base.metadata.create_all(bind=engine)