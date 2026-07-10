from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from src.schemas.project_graph import GraphNode, ProjectGraph


# ============================================================
# Result Models
# ============================================================

@dataclass
class ScheduleMetrics:
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    not_started_tasks: int

    planned_duration_days: int

    average_progress: float

    delayed_tasks: int

    completed_percentage: float


# ============================================================
# Schedule Engine
# ============================================================

class ScheduleEngine:
    """
    Performs schedule analytics on ProjectGraph.

    Computes

        • Progress

        • Duration

        • Delay

        • Completion %

    """

    # --------------------------------------------------------

    def analyze(
        self,
        graph: ProjectGraph,
    ) -> ScheduleMetrics:

        tasks = graph.by_type("task")

        total = len(tasks)

        completed = 0
        progress = 0

        delayed = 0

        in_progress = 0

        not_started = 0

        durations = []

        today = datetime.today().date()

        for task in tasks:

            props = task.properties

            status = str(
                props.get("status", "")
            ).lower()

            if status == "completed":
                completed += 1

            elif status == "in progress":
                in_progress += 1

            else:
                not_started += 1

            progress += float(
                props.get(
                    "progress",
                    0,
                )
            )

            duration = props.get("duration")

            if isinstance(
                duration,
                (int, float),
            ):

                durations.append(duration)

            planned_end = props.get(
                "planned_end"
            )

            if planned_end:

                try:

                    if (
                        planned_end.date()
                        < today
                        and status != "completed"
                    ):

                        delayed += 1

                except Exception:
                    pass

        average_progress = (
            progress / total
            if total
            else 0
        )

        completed_percentage = (
            completed * 100 / total
            if total
            else 0
        )

        planned_duration = (
            int(sum(durations))
            if durations
            else 0
        )

        return ScheduleMetrics(

            total_tasks=total,

            completed_tasks=completed,

            in_progress_tasks=in_progress,

            not_started_tasks=not_started,

            planned_duration_days=planned_duration,

            average_progress=round(
                average_progress,
                2,
            ),

            delayed_tasks=delayed,

            completed_percentage=round(
                completed_percentage,
                2,
            ),
        )

    # --------------------------------------------------------

    @staticmethod
    def print_report(
        metrics: ScheduleMetrics,
    ):

        print("\n")

        print("=" * 70)

        print("PROJECT SCHEDULE REPORT")

        print("=" * 70)

        print(
            f"Total Tasks        : {metrics.total_tasks}"
        )

        print(
            f"Completed          : {metrics.completed_tasks}"
        )

        print(
            f"In Progress        : {metrics.in_progress_tasks}"
        )

        print(
            f"Not Started        : {metrics.not_started_tasks}"
        )

        print(
            f"Delayed Tasks      : {metrics.delayed_tasks}"
        )

        print(
            f"Average Progress   : {metrics.average_progress:.2f}%"
        )

        print(
            f"Completion %       : {metrics.completed_percentage:.2f}%"
        )

        print(
            f"Planned Duration   : {metrics.planned_duration_days} days"
        )

        print("=" * 70)