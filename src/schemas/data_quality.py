from pydantic import BaseModel
from typing import List, Optional

class DataQualityIssueSchema(BaseModel):
    issue_type: str
    severity: str
    description: str
    entity_type: Optional[str] = None
    entity_name: Optional[str] = None

class DataQualityReportSchema(BaseModel):
    completeness_score: float
    data_confidence_score: float
    total_issues: int
    issues: List[DataQualityIssueSchema] = []