from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.project_context import ProjectContext
from src.models.project import Project, Phase, Milestone, Task, TaskStatus, ScheduleHealth
from src.models.comment import Comment
from src.models.summary import Summary

class ProjectPersistenceService:
    """Persists a fully‑normalised ProjectContext into the database. Returns project ID."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def persist(self, ctx: ProjectContext) -> int:
        project = Project(
            name=ctx.project_name,
            project_manager=ctx.project_manager,
            category=ctx.category,
        )
        self.session.add(project)
        await self.session.flush()

        for phase_ctx in ctx.phases:
            phase = Phase(
                project_id=project.id,
                name=phase_ctx.name,
                start_date=phase_ctx.start_date,
                end_date=phase_ctx.end_date,
                audit_raw_data=phase_ctx.audit_raw_data,
            )
            self.session.add(phase)
            await self.session.flush()

            for ms_ctx in phase_ctx.milestones:
                ms = Milestone(
                    phase_id=phase.id,
                    name=ms_ctx.name,
                    planned_start=ms_ctx.planned_start,
                    planned_end=ms_ctx.planned_end,
                    status=self._to_task_status(ms_ctx.status),
                    schedule_health=self._to_schedule_health(ms_ctx.schedule_health),
                    audit_raw_data=ms_ctx.audit_raw_data,
                )
                self.session.add(ms)
                await self.session.flush()

                for t_ctx in ms_ctx.tasks:
                    task = Task(
                        milestone_id=ms.id,
                        name=t_ctx.name,
                        description=t_ctx.description,
                        owner=t_ctx.owner,
                        status=self._to_task_status(t_ctx.status),
                        percent_complete=t_ctx.percent_complete,
                        planned_start=t_ctx.planned_start,
                        planned_end=t_ctx.planned_end,
                        duration=t_ctx.duration,
                        schedule_health=self._to_schedule_health(t_ctx.schedule_health),
                        at_risk=t_ctx.at_risk,
                        on_hold=t_ctx.on_hold,
                        not_applicable=t_ctx.not_applicable,
                        predecessors=", ".join(t_ctx.dependencies) if t_ctx.dependencies else None,
                        audit_raw_data=t_ctx.audit_raw_data,
                    )
                    self.session.add(task)

        for c in ctx.comments:
            self.session.add(Comment(project_id=project.id, text=c.text, author=c.author))

        summary = Summary(
            project_id=project.id,
            project_start=ctx.summary.project_start,
            project_end=ctx.summary.project_end,
            total_tasks=ctx.summary.total_tasks,
            completed_tasks=ctx.summary.completed_tasks,
            in_progress_tasks=ctx.summary.in_progress_tasks,
            not_started_tasks=ctx.summary.not_started_tasks,
        )
        self.session.add(summary)
        await self.session.flush()
        logger.info("Persisted project id={} with {} phases.", project.id, len(ctx.phases))
        return project.id

    @staticmethod
    def _to_task_status(value: str | None) -> TaskStatus:
        if value is None:
            return TaskStatus.NOT_STARTED
        mapping = {
            "completed": TaskStatus.COMPLETED,
            "in progress": TaskStatus.IN_PROGRESS,
            "not started": TaskStatus.NOT_STARTED,
        }
        return mapping.get(value.lower(), TaskStatus.NOT_STARTED)

    @staticmethod
    def _to_schedule_health(value: str | None) -> ScheduleHealth | None:
        if value is None:
            return None
        mapping = {
            "green": ScheduleHealth.GREEN,
            "yellow": ScheduleHealth.YELLOW,
            "red": ScheduleHealth.RED,
        }
        return mapping.get(value.lower())