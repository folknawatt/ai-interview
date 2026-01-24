from app.database.db import engine, init_db
from sqlmodel import SQLModel
import sys
import os
import logging

# Add parent dir to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset():
    print("⚠️  WARNING: This will drop ALL data in the database.")
    confirm = input("Are you sure? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    print("🗑️  Dropping all tables...", end=" ", flush=True)
    try:
        SQLModel.metadata.drop_all(bind=engine)
        print("✅ Done")
    except Exception as e:
        print(f"\n❌ Error dropping tables: {e}")
        return

    print("🌱 Re-initializing and seeding database...", end=" ", flush=True)
    try:
        init_db()
        print("✅ Done")
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        return

    print("\n✨ Database reset successfully! Base roles have been restored.")


if __name__ == "__main__":
    reset()
