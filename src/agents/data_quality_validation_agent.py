from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.data_quality import DataQualityReportSchema
from src.schemas.project_context import ProjectContext
from src.services.validation_service import ValidationService


class DataQualityValidationAgent:
    """
    Validates the ingested project context and returns a
    Data Quality Report DTO (Pydantic), not an ORM entity.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(
        self,
        project_id: int,
        ctx: ProjectContext,
    ) -> DataQualityReportSchema:
        return await ValidationService.validate(
            ctx=ctx,
            session=self.session,
            project_id=project_id,
        )