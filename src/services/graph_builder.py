from __future__ import annotations

from typing import Optional
from uuid import uuid4

from src.schemas.project_context import (
    ProjectContext,
    PhaseContext,
    MilestoneContext,
    TaskContext,
)

from src.schemas.project_graph import (
    GraphNode,
    ProjectGraph,
)


class GraphBuilder:
    """
    Converts ProjectContext into a graph representation.

    Project
        ↓
    Phase
        ↓
    Milestone
        ↓
    Task

    Every node receives a unique ID and parent-child links.
    """

    # =====================================================

    def build(
        self,
        context: ProjectContext,
    ) -> ProjectGraph:

        graph = ProjectGraph(
            project_name=context.project_name
        )

        # --------------------------------------------
        # Project Node
        # --------------------------------------------

        project_id = self._new_id()

        graph.root_id = project_id

        graph.add_node(
            GraphNode(
                id=project_id,
                node_type="project",
                name=context.project_name,
                properties={
                    "project_manager": context.project_manager,
                    "category": context.category,
                },
            )
        )

        # --------------------------------------------
        # Phases
        # --------------------------------------------

        for phase in context.phases:

            self._add_phase(
                graph,
                phase,
                parent_id=project_id,
            )

        return graph

    # =====================================================

    def _add_phase(
        self,
        graph: ProjectGraph,
        phase: PhaseContext,
        parent_id: str,
    ):

        phase_id = self._new_id()

        graph.add_node(
            GraphNode(
                id=phase_id,
                node_type="phase",
                name=phase.name,
                parent=parent_id,
                properties={
                    "start_date": phase.start_date,
                    "end_date": phase.end_date,
                },
            )
        )

        graph.get(parent_id).children.append(
            phase_id
        )

        for milestone in phase.milestones:

            self._add_milestone(
                graph,
                milestone,
                phase_id,
            )

    # =====================================================

    def _add_milestone(
        self,
        graph: ProjectGraph,
        milestone: MilestoneContext,
        parent_id: str,
    ):

        milestone_id = self._new_id()

        graph.add_node(
            GraphNode(
                id=milestone_id,
                node_type="milestone",
                name=milestone.name,
                parent=parent_id,
                properties={
                    "status": milestone.status,
                    "planned_start": milestone.planned_start,
                    "planned_end": milestone.planned_end,
                    "schedule_health": milestone.schedule_health,
                },
            )
        )

        graph.get(parent_id).children.append(
            milestone_id
        )

        for task in milestone.tasks:

            self._add_task(
                graph,
                task,
                milestone_id,
            )

    # =====================================================

    def _add_task(
        self,
        graph: ProjectGraph,
        task: TaskContext,
        parent_id: str,
    ):

        task_id = self._new_id()

        graph.add_node(
            GraphNode(
                id=task_id,
                node_type="task",
                name=task.name,
                parent=parent_id,
                properties={
                    "owner": task.owner,
                    "status": task.status,
                    "progress": task.percent_complete,
                    "planned_start": task.planned_start,
                    "planned_end": task.planned_end,
                    "duration": task.duration,
                    "dependencies": task.dependencies,
                    "schedule_health": task.schedule_health,
                    "at_risk": task.at_risk,
                    "on_hold": task.on_hold,
                },
            )
        )

        graph.get(parent_id).children.append(
            task_id
        )

    # =====================================================

    @staticmethod
    def _new_id() -> str:
        return str(uuid4())

    # =====================================================

    @staticmethod
    def print_graph(
        graph: ProjectGraph,
    ) -> None:

        if graph.root_id is None:
            return

        def dfs(
            node_id: str,
            level: int,
        ):

            node = graph.get(node_id)

            if node is None:
                return

            print(
                "    " * level
                + f"{node.node_type.upper()} : {node.name}"
            )

            for child in node.children:

                dfs(
                    child,
                    level + 1,
                )

        dfs(
            graph.root_id,
            0,
        )