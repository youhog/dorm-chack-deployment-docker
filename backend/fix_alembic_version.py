"""
Temporary script to fix alembic version mismatch
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERROR: DATABASE_URL not found in environment")
    exit(1)

# Create engine
engine = create_engine(database_url)

# Update alembic_version to current head
with engine.connect() as conn:
    # Delete old version
    conn.execute(text("DELETE FROM alembic_version"))
    # Insert current version (503107688e81 is the latest)
    conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('503107688e81')"))
    conn.commit()
    print("Successfully updated alembic_version to 503107688e81")
