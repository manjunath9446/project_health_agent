from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=20,
    max_overflow=0,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


# =====================================================
# Create Database Tables
# =====================================================

async def init_db():

    # Import ALL models before create_all()

    from src.models.project import (
        Project,
        Phase,
        Milestone,
        Task,
    )

    from src.models.summary import Summary

    from src.models.comment import Comment

    from src.models.project_analysis import ProjectAnalysis

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    print("Database initialized successfully.")