from sqlalchemy import text

async def init_db():

    import src.models.project
    import src.models.summary
    import src.models.comment
    import src.models.project_analysis

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")
        )

        print("Tables:", result.fetchall())

    print("✅ Database initialized.")