import pytest
from src.services.validation_service import ValidationService
from src.schemas.project_context import ProjectContext, PhaseContext, MilestoneContext, TaskContext

@pytest.mark.asyncio
async def test_duplicate_task_detection(db_session):
    ctx = ProjectContext(
        project_name="Test",
        project_manager="PM",
        category="IT",
        phases=[
            PhaseContext(name="P1", milestones=[
                MilestoneContext(name="M1", tasks=[
                    TaskContext(name="Task1", status="Completed", percent_complete=100),
                    TaskContext(name="Task1", status="In Progress", percent_complete=50)
                ])
            ])
        ]
    )
    report = await ValidationService.validate(ctx, db_session, project_id=1)
    assert report.total_issues >= 1
    assert any(i.issue_type == "duplicate_task" for i in report.issues)