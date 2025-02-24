import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from a .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Connects SQLAlchemy to the database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# Session which will be use to query the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define ORM (Object-Relational Mapping) models that will interact with the database tables
Base = declarative_base()

def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide the session to the caller
    finally:
        db.close()  # Close the session after use