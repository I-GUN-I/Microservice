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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()