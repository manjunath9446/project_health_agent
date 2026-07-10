from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TaskContext(BaseModel):
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    status: str
    percent_complete: float
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    duration: Optional[int] = None
    schedule_health: Optional[str] = None
    at_risk: bool = False
    on_hold: bool = False
    not_applicable: bool = False
    dependencies: List[str] = []
    audit_raw_data: dict = {}

class MilestoneContext(BaseModel):
    name: str
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: Optional[str] = None
    schedule_health: Optional[str] = None
    tasks: List[TaskContext] = []
    audit_raw_data: dict = {}

class PhaseContext(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    milestones: List[MilestoneContext] = []
    audit_raw_data: dict = {}

class CommentContext(BaseModel):
    text: str
    author: Optional[str] = None

class SummaryContext(BaseModel):
    project_start: Optional[datetime] = None
    project_end: Optional[datetime] = None
    total_tasks: int = 0
    completed_tasks: int = 0
    in_progress_tasks: int = 0
    not_started_tasks: int = 0

class ProjectContext(BaseModel):
    project_name: str
    project_manager: str
    category: str
    phases: List[PhaseContext] = []
    comments: List[CommentContext] = []
    summary: SummaryContext = SummaryContext()