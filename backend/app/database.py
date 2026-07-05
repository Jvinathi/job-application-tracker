from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Try environment variable first, then fall back to hardcoded Railway URL
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # Hardcoded Railway public URL as fallback
    DATABASE_URL = "mysql+pymysql://root:RZpZxrYDReQFXmTRjeuaCSTyBtMlsGaE@thomas.proxy.rlwy.net:24219/railway"

# Fix URL prefix if needed
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

print(f"[DB] Connecting to: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()