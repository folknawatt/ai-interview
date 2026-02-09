import asyncio
import os
import sys
import logging
from sqlalchemy import text
from sqlmodel import SQLModel

# Add parent dir to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import engine, init_db  # noqa: E402

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def reset():
    print("⚠️  WARNING: This will drop ALL data in the database.")
    confirm = input("Are you sure? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    print("🗑️  Dropping all tables...", end=" ", flush=True)
    try:
        async with engine.begin() as conn:
            # Disable foreign key checks to allow dropping tables in any order
            await conn.execute(text("DROP SCHEMA public CASCADE;"))
            await conn.execute(text("CREATE SCHEMA public;"))
            # Alternative if we want to keep schema:
            # await conn.run_sync(SQLModel.metadata.drop_all)
        print("✅ Done")
    except Exception as e:
        print(f"\n❌ Error dropping tables: {e}")
        return

    print("🌱 Re-initializing and seeding database...", end=" ", flush=True)
    try:
        await init_db()
        print("✅ Done")
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        return

    print("\n✨ Database reset successfully! Base roles have been restored.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(reset())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
