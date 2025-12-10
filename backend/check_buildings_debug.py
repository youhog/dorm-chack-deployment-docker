import asyncio
from sqlalchemy import text
from app.database import AsyncSessionLocal

async def check_buildings():
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(text("SELECT id, name FROM buildings"))
            buildings = result.fetchall()
            print(f"Total buildings found: {len(buildings)}")
            for b in buildings:
                print(f"ID: {b.id}, Name: {b.name}")
        except Exception as e:
            print(f"Error checking buildings: {e}")

if __name__ == "__main__":
    asyncio.run(check_buildings())