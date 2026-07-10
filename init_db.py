import asyncio

from src.core.database import init_db


asyncio.run(init_db())