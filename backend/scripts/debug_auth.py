from app.config.settings import settings
from app.services.auth.auth_service import AuthService
from app.database.models import HRUser
from app.database.db import engine
import asyncio
import sys
import os
import logging
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Add parent dir to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def debug_auth():
    logger.info("Starting debug_auth function")
    try:
        async with AsyncSession(engine) as session:
            logger.info("Checking for admin user...")
            statement = select(HRUser).where(HRUser.username == "admin")
            result = await session.exec(statement)
            user = result.first()

            if not user:
                logger.error("Admin user NOT found!")
                return

            logger.info(
                f"Admin user found: {user.username} (Email: {user.email})")

            expected_pass = settings.admin_default_password

            is_valid = AuthService.verify_password(
                expected_pass, user.hashed_password)
            logger.info(f"Password '{expected_pass}' is valid? {is_valid}")

            if not is_valid:
                logger.warning("Password mismatch! Resetting now...")
                new_hash = AuthService.get_password_hash(expected_pass)
                user.hashed_password = new_hash
                session.add(user)
                await session.commit()
                logger.info("Password has been forcefully reset.")

                # Verify again
                is_valid_now = AuthService.verify_password(
                    expected_pass, user.hashed_password)
                logger.info(f"Verification after reset: {is_valid_now}")
            else:
                logger.info("Password is correct. Login should work.")
    except Exception as e:
        logger.error(f"Exception caught: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(debug_auth())
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
