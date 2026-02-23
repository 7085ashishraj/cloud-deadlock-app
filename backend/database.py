import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fallback to SQLite if MySQL isn't configured for easy local dev
# Change this to your MySQL URI: mysql+mysqlconnector://user:password@localhost/deadlock_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./deadlock.db")

engine = create_engine(
    DATABASE_URL, 
    # check_same_thread is needed only for SQLite
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
