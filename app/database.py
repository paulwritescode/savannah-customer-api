from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Use SQLite for development to avoid PostgreSQL installation issues
database_url = os.getenv("DATABASE_URL", "sqlite:///./savannah_orders.db")

engine = create_engine(
    database_url,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
