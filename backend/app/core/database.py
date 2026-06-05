from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Do not connect to PostgreSQL synchronously if using asyncpg, but the instructions ask for standard SessionLocal setup.
# In a real app we might use create_async_engine. Given the requirements.txt has psycopg2-binary and asyncpg, we will provide standard sync setup. If needed async can be swapped later.

engine = create_engine(
    settings.DATABASE_URL, 
    # pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
