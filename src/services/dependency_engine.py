from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

from src.schemas.project_graph import ProjectGraph, GraphNode


# ==========================================================
# Result Models
# ==========================================================

@dataclass
class DependencyIssue:
    issue_type: str
    task: str
    dependency: str | None
    message: str


@dataclass
class DependencyReport:

    total_dependencies: int = 0

    missing_dependencies: List[DependencyIssue] = field(default_factory=list)

    circular_dependencies: List[DependencyIssue] = field(default_factory=list)

    self_dependencies: List[DependencyIssue] = field(default_factory=list)

    orphan_tasks: List[str] = field(default_factory=list)


# ==========================================================
# Engine
# ==========================================================

class DependencyEngine:

    """
    Analyse task dependencies.

    Detects

        Missing predecessors

        Circular dependencies

        Self dependency

        Orphan tasks
    """

    # ------------------------------------------------------

    def analyze(
        self,
        graph: ProjectGraph,
    ) -> DependencyReport:

        report = DependencyReport()

        tasks = graph.by_type("task")

        lookup = {}

        # ------------------------------------
        # Build lookup
        # ------------------------------------

        for task in tasks:

            lookup[task.name.strip().lower()] = task

        # ------------------------------------
        # Missing / Self
        # ------------------------------------

        for task in tasks:

            deps = task.properties.get(
                "dependencies",
                [],
            )

            if deps is None:
                deps = []

            if not isinstance(deps, list):
                deps = [deps]

            if len(deps) == 0:

                report.orphan_tasks.append(
                    task.name
                )

            for dep in deps:

                report.total_dependencies += 1

                dep_name = str(dep).strip().lower()

                if dep_name == task.name.strip().lower():

                    report.self_dependencies.append(

                        DependencyIssue(

                            issue_type="SELF_DEPENDENCY",

                            task=task.name,

                            dependency=dep,

                            message="Task depends on itself.",
                        )
                    )

                if dep_name not in lookup:

                    report.missing_dependencies.append(

                        DependencyIssue(

                            issue_type="MISSING_DEPENDENCY",

                            task=task.name,

                            dependency=dep,

                            message="Referenced predecessor not found.",
                        )
                    )

        # ------------------------------------
        # Circular Dependency
        # ------------------------------------

        graph_map = {}

        for task in tasks:

            deps = task.properties.get(
                "dependencies",
                [],
            )

            graph_map[
                task.name.strip().lower()
            ] = [

                str(d).strip().lower()

                for d in deps
            ]

        visited = set()

        stack = set()

        for node in graph_map.keys():

            self._dfs(

                node,

                graph_map,

                visited,

                stack,

                report,
            )

        return report

    # ------------------------------------------------------

    def _dfs(

        self,

        node: str,

        graph: Dict[str, List[str]],

        visited: Set[str],

        stack: Set[str],

        report: DependencyReport,

    ):

        if node in stack:

            report.circular_dependencies.append(

                DependencyIssue(

                    issue_type="CIRCULAR_DEPENDENCY",

                    task=node,

                    dependency=node,

                    message="Circular dependency detected.",
                )
            )

            return

        if node in visited:
            return

        visited.add(node)

        stack.add(node)

        for child in graph.get(node, []):

            if child in graph:

                self._dfs(

                    child,

                    graph,

                    visited,

                    stack,

                    report,
                )

        stack.remove(node)

    # ------------------------------------------------------

    @staticmethod
    def print_report(
        report: DependencyReport,
    ):

        print()

        print("=" * 70)

        print("DEPENDENCY REPORT")

        print("=" * 70)

        print(
            "Total Dependencies :",
            report.total_dependencies,
        )

        print(
            "Missing            :",
            len(report.missing_dependencies),
        )

        print(
            "Circular           :",
            len(report.circular_dependencies),
        )

        print(
            "Self Dependency    :",
            len(report.self_dependencies),
        )

        print(
            "Orphan Tasks       :",
            len(report.orphan_tasks),
        )

        print("=" * 70)