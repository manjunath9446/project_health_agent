from sqlalchemy.ext.asyncio import AsyncSession
from src.services.ingestion_service import IngestionService
from src.schemas.project_context import ProjectContext

class IngestionNormalizationAgent:
    def __init__(self, session: AsyncSession):
        self.service = IngestionService(session)
    async def execute(self, file_path: str, project_name: str) -> tuple[int, ProjectContext]:
        return await self.service.ingest(file_path, project_name)