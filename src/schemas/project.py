from pydantic import BaseModel
from typing import Optional
from .data_quality import DataQualityReportSchema

class ProjectUploadResponse(BaseModel):
    project_id: int
    project_name: str
    status: str
    message: str
    data_quality_report: Optional[DataQualityReportSchema] = None