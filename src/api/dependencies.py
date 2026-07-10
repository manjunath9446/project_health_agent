from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.agents.coordinator import CoordinatorAgent

async def get_coordinator(db: AsyncSession = Depends(get_db)) -> CoordinatorAgent:
    return CoordinatorAgent(db)