from app.services.auth.auth_service import AuthService
from app.database.models import HRUser, UserRole
from app.database.db import engine
import asyncio
import sys
import os
import logging
import getpass
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Add parent dir to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


async def create_admin():
    print("\n--- Create New Admin User ---\n")

    # Interactive Input
    try:
        username = input("Username: ").strip()
        if not username:
            print("Error: Username cannot be empty.")
            return

        email = input("Email: ").strip()
        if not email:
            print("Error: Email cannot be empty.")
            return

        full_name = input("Full Name (Optional): ").strip()
        if not full_name:
            full_name = "Admin User"

        password = getpass.getpass("Password: ")
        if not password:
            print("Error: Password cannot be empty.")
            return

        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("Error: Passwords do not match.")
            return

    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        return

    print(f"\nCreating user '{username}' ({email})...")

    try:
        async with AsyncSession(engine) as session:
            # Check if exists
            existing_user = await AuthService.get_user_by_username(session, username)
            if existing_user:
                print(
                    f"Error: User with username '{username}' already exists.")
                return

            # Create user
            await AuthService.create_user(
                session=session,
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                role=UserRole.ADMIN
            )
            print(f"\n✅ Admin user '{username}' created successfully!")

    except Exception as e:
        # Check for specific validation errors if possible
        if "already exists" in str(e):
            print(f"Error: {e}")
        else:
            logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(create_admin())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
