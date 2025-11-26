import sys
import os
import asyncio
from sqlalchemy import text

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.database import async_session_maker

async def check_announcements():
    async with async_session_maker() as db:
        try:
            # Check if table exists
            result = await db.execute(text("SHOW TABLES LIKE 'announcements'"))
            table_exists = result.scalar()
            print(f"Table 'announcements' exists: {table_exists}")

            if table_exists:
                # Check count
                result = await db.execute(text("SELECT COUNT(*) FROM announcements"))
                count = result.scalar()
                print(f"Announcement count: {count}")
                
                if count > 0:
                    result = await db.execute(text("SELECT id, title, is_active FROM announcements LIMIT 5"))
                    rows = result.fetchall()
                    for row in rows:
                        print(f" - {row}")
            else:
                print("Table does not exist!")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_announcements())
