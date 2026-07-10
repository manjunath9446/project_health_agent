from __future__ import annotations

from typing import Any, Dict, List

from src.schemas.project_context import (
    CommentContext,
    MilestoneContext,
    PhaseContext,
    ProjectContext,
    SummaryContext,
    TaskContext,
)

from src.services.node_classifier import (
    NodeClassifier,
    ClassifiedNode,
)

from src.services.normalization import Normalizer
from src.utils.json_utils import make_json_serializable
class ProjectContextBuilder:

    def __init__(
        self,
        project_name: str,
        project_manager: str,
        category: str,
        hierarchy_roots,
        comments_raw: List[Dict[str, Any]],
        summary_raw: Dict[str, Any],
    ):

        self.project_name = project_name
        self.project_manager = project_manager
        self.category = category

        self.comments_raw = comments_raw
        self.summary_raw = summary_raw

        classifier = NodeClassifier()

        self.roots: List[ClassifiedNode] = classifier.classify(
            hierarchy_roots
        )

    # =========================================================

    def build(self) -> ProjectContext:

        phases = []

        for project in self.roots:

            if project.node_type != "project":
                continue

            for phase in project.children:

                if phase.node_type != "phase":
                    continue

                phases.append(
                    self._build_phase(phase)
                    )

        comments = self._build_comments()

        summary = self._build_summary()

        return ProjectContext(

            project_name=self.project_name,

            project_manager=self.project_manager,

            category=self.category,

            phases=phases,

            comments=comments,

            summary=summary,
        )

    # =========================================================

    def _build_comments(
        self,
    ) -> List[CommentContext]:

        comments = []

        for item in self.comments_raw:

            comments.append(

                CommentContext(

                    text=str(
                        item.get(
                            "text",
                            "",
                        )
                    ),

                    author=item.get(
                        "author"
                    ),
                )
            )

        return comments

    # =========================================================

    def _build_summary(
        self,
    ) -> SummaryContext:

        summary = Normalizer.normalize_summary(
            self.summary_raw
        )

        return SummaryContext(

            project_start=summary.get(
                "normalized_project_start"
            ),

            project_end=summary.get(
                "normalized_project_end"
            ),

            total_tasks=summary.get(
                "normalized_total_tasks",
                0,
            ),

            completed_tasks=summary.get(
                "normalized_completed_tasks",
                0,
            ),

            in_progress_tasks=summary.get(
                "normalized_in_progress_tasks",
                0,
            ),

            not_started_tasks=summary.get(
                "normalized_not_started_tasks",
                0,
            ),
        )

    # =========================================================

    def _build_phase(
        self,
        node: ClassifiedNode,
    ) -> PhaseContext:

        milestones = []

        general_tasks = []

        for child in node.children:

            if child.node_type == "milestone":

                milestones.append(
                self._build_milestone(child)
                )

            elif child.node_type == "task":

                general_tasks.append(
                self._build_task(child)
                )

        if general_tasks:

            milestones.insert(
            0,
            MilestoneContext(
                name="General Tasks",
                planned_start=None,
                planned_end=None,
                status=None,
                schedule_health=None,
                tasks=general_tasks,
                audit_raw_data={},
            ),
        )

        raw = node.node.raw_data

        return PhaseContext(

            name=node.node.name,

            start_date=raw.get(
                "normalized_planned_start"
            ),

            end_date=raw.get(
                "normalized_planned_end"
            ),

            milestones=milestones,

            audit_raw_data=make_json_serializable(
                raw
            ),
        )
        # =========================================================

    def _build_milestone(
        self,
        node: ClassifiedNode,
    ) -> MilestoneContext:

        raw = node.node.raw_data

        tasks = self._collect_tasks_recursive(node)

        return MilestoneContext(

            name=node.node.name,

            planned_start=raw.get(
                "normalized_planned_start"
            ),

            planned_end=raw.get(
                "normalized_planned_end"
            ),

            status=raw.get(
                "normalized_status"
            ),

            schedule_health=raw.get(
                "normalized_schedule_health"
            ),

            tasks=tasks,

            audit_raw_data=make_json_serializable(
                raw
            ),
        )

    # =========================================================

    def _collect_tasks_recursive(
        self,
        node: ClassifiedNode,
    ) -> List[TaskContext]:

        """
        Recursively collect every task under a milestone.

        Handles:

        Milestone
            ├── Task
            ├── Task
            ├── Task
            │     ├── Task
            │     └── Task
            └── Task

        Unlimited depth.
        """

        tasks: List[TaskContext] = []

        for child in node.children:

            if child.node_type == "task":

                tasks.append(
                    self._build_task(child)
                )
            if child.children:


            # Continue searching deeper regardless
                tasks.extend(
                    self._collect_tasks_recursive(
                        child
                    )
                )

        return tasks

    # =========================================================

    def _build_task(
        self,
        node: ClassifiedNode,
    ) -> TaskContext:

        raw = node.node.raw_data

        return TaskContext(

            name=node.node.name,

            description=raw.get(
                "normalized_description"
            ),

            owner=raw.get(
                "normalized_owner"
            ),

            status=raw.get(
                "normalized_status",
                "Not Started",
            ),

            percent_complete=raw.get(
                "normalized_percent_complete",
                0.0,
            ),

            planned_start=raw.get(
                "normalized_planned_start"
            ),

            planned_end=raw.get(
                "normalized_planned_end"
            ),

            duration=raw.get(
                "normalized_duration"
            ),

            schedule_health=raw.get(
                "normalized_schedule_health"
            ),

            at_risk=raw.get(
                "normalized_at_risk",
                False,
            ),

            on_hold=raw.get(
                "normalized_on_hold",
                False,
            ),

            not_applicable=raw.get(
                "normalized_not_applicable",
                False,
            ),

            dependencies=raw.get(
                "normalized_dependencies",
                [],
            ),

            audit_raw_data=make_json_serializable(
                raw
            ),
        )