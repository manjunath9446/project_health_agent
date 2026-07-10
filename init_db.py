async def init_db():

    import src.models.project
    import src.models.comment
    import src.models.summary
    import src.models.project_analysis

    print("=" * 80)
    print("REGISTERED TABLES")
    print(Base.metadata.tables.keys())
    print("=" * 80)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DATABASE INITIALIZED")