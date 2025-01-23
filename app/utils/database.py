"""
Database connection and setup utilities.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_NAME = DATABASE_URL.rsplit("/", 1)[-1]

root_engine = create_engine(DATABASE_URL.rsplit("/", 1)[0] + "/")

with root_engine.connect() as conn:
    if not conn.execute(
        text(f"SHOW DATABASES LIKE '{DATABASE_NAME}'")
    ).fetchone():
        conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
        print(f"Database '{DATABASE_NAME}' created.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
