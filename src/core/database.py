from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

# ----------------------------------------------------
# Database Engine
# ----------------------------------------------------

engine = create_async_engine(
    settings.database_url,
    echo=False,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ----------------------------------------------------
# Base Class
# ----------------------------------------------------

class Base(DeclarativeBase):
    pass

# ----------------------------------------------------
# Dependency
# ----------------------------------------------------

async def get_db():

    async with async_session() as session:
        yield session

# ----------------------------------------------------
# Initialize Database
# ----------------------------------------------------

async def init_db():

    # Import ALL models so SQLAlchemy registers them

    import src.models.project
    import src.models.summary
    import src.models.comment
    import src.models.project_analysis

    async with engine.begin() as conn:

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized successfully.")