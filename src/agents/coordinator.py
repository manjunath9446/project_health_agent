from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.ingestion_normalization_agent import IngestionNormalizationAgent
from src.agents.data_quality_validation_agent import DataQualityValidationAgent
from src.schemas.project_context import ProjectContext
from src.models.data_quality import DataQualityReport

class CoordinatorAgent:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ingestion = IngestionNormalizationAgent(session)
        self.validation = DataQualityValidationAgent(session)

    async def process_upload(self, file_path: str, project_name: str) -> tuple[int, ProjectContext, DataQualityReport]:
        proj_id, ctx = await self.ingestion.execute(file_path, project_name)
        report = await self.validation.execute(proj_id, ctx)
        return proj_id, ctx, report