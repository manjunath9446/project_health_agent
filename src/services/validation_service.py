from collections import Counter

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.data_quality import (
    DataQualityIssue,
    DataQualityReport,
)
from src.schemas.data_quality import (
    DataQualityIssueSchema,
    DataQualityReportSchema,
)
from src.schemas.project_context import ProjectContext


class ValidationService:
    @staticmethod
    async def validate(
        ctx: ProjectContext,
        session: AsyncSession,
        project_id: int,
    ) -> DataQualityReportSchema:

        issues: list[DataQualityIssue] = []

        # =====================================================
        # Duplicate Tasks
        # =====================================================
        for phase in ctx.phases:
            for milestone in phase.milestones:

                names = [task.name for task in milestone.tasks]

                duplicates = [
                    name
                    for name, count in Counter(names).items()
                    if count > 1
                ]

                for duplicate in duplicates:
                    issues.append(
                        DataQualityIssue(
                            issue_type="duplicate_task",
                            severity="error",
                            description=f"Duplicate task '{duplicate}' found in milestone '{milestone.name}'.",
                            entity_type="Task",
                            entity_name=duplicate,
                        )
                    )

        # =====================================================
        # Task Validation
        # =====================================================
        for phase in ctx.phases:
            for milestone in phase.milestones:
                for task in milestone.tasks:

                    # Missing Dates
                    if not task.planned_start or not task.planned_end:
                        issues.append(
                            DataQualityIssue(
                                issue_type="missing_date",
                                severity="warning",
                                description=f"Task '{task.name}' is missing planned dates.",
                                entity_type="Task",
                                entity_name=task.name,
                            )
                        )

                    # Inconsistent Progress
                    if (
                        task.status == "In Progress"
                        and task.percent_complete == 0
                    ):
                        issues.append(
                            DataQualityIssue(
                                issue_type="inconsistent_status",
                                severity="warning",
                                description=f"Task '{task.name}' is marked In Progress but completion is 0%.",
                                entity_type="Task",
                                entity_name=task.name,
                            )
                        )

                    # Invalid Schedule Health
                    if (
                        task.schedule_health
                        and task.schedule_health
                        not in ("Green", "Yellow", "Red")
                    ):
                        issues.append(
                            DataQualityIssue(
                                issue_type="invalid_schedule_health",
                                severity="error",
                                description=f"Task '{task.name}' has invalid schedule health '{task.schedule_health}'.",
                                entity_type="Task",
                                entity_name=task.name,
                            )
                        )

                    # Invalid Date Range
                    if (
                        task.planned_start
                        and task.planned_end
                        and task.planned_end < task.planned_start
                    ):
                        issues.append(
                            DataQualityIssue(
                                issue_type="invalid_date_range",
                                severity="error",
                                description=f"Task '{task.name}' has end date before start date.",
                                entity_type="Task",
                                entity_name=task.name,
                            )
                        )

        # =====================================================
        # Metrics
        # =====================================================
        total_tasks = sum(
            len(m.tasks)
            for p in ctx.phases
            for m in p.milestones
        )

        tasks_with_dates = sum(
            1
            for p in ctx.phases
            for m in p.milestones
            for t in m.tasks
            if t.planned_start and t.planned_end
        )

        completeness = (
            tasks_with_dates / total_tasks
            if total_tasks > 0
            else 1.0
        )

        error_count = sum(
            1 for issue in issues if issue.severity == "error"
        )

        warning_count = sum(
            1 for issue in issues if issue.severity == "warning"
        )

        confidence = max(
            0.0,
            1.0 - (error_count * 0.20 + warning_count * 0.10),
        )

        # =====================================================
        # Persist Report
        # =====================================================
        report = DataQualityReport(
            project_id=project_id,
            completeness_score=round(completeness, 3),
            data_confidence_score=round(confidence, 3),
            total_issues=len(issues),
        )

        session.add(report)
        await session.flush()

        for issue in issues:
            issue.report_id = report.id

        session.add_all(issues)

        await session.flush()
        await session.commit()
        print("\nVALIDATION ISSUES")

        for issue in issues:
            print(issue)

        logger.success(
            "Validation completed. {} issue(s) detected.",
            len(issues),
        )

        # =====================================================
        # Return DTO (NOT ORM)
        # =====================================================
        return DataQualityReportSchema(
            completeness_score=report.completeness_score,
            data_confidence_score=report.data_confidence_score,
            total_issues=report.total_issues,
            issues=[
                DataQualityIssueSchema(
                    issue_type=issue.issue_type,
                    severity=issue.severity,
                    description=issue.description,
                    entity_type=issue.entity_type,
                    entity_name=issue.entity_name,
                )
                for issue in issues
            ],
        )