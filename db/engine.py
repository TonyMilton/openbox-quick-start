import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL with psycopg2
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create synchronous engine for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)

@contextmanager
def get_db_session():
    """Context manager for database sessions with auto-commit/rollback."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Initialize database tables (idempotent, safe for development)."""
    from db.models import Base

    Base.metadata.create_all(bind=engine)
