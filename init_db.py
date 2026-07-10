async def init_db():

    # Import all models so SQLAlchemy registers them
    import src.models.project
    import src.models.summary
    import src.models.comment
    import src.models.project_analysis

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized.")