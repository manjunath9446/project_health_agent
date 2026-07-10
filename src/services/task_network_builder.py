from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from src.schemas.project_graph import ProjectGraph


# ============================================================
# Task Network Models
# ============================================================

@dataclass
class TaskVertex:
    """
    Represents one task in the scheduling network.
    """

    id: str

    name: str

    duration: float = 0.0

    planned_start: Optional[datetime] = None

    planned_end: Optional[datetime] = None

    owner: Optional[str] = None

    status: Optional[str] = None

    progress: float = 0.0

    schedule_health: Optional[str] = None

    predecessors: List[str] = field(default_factory=list)

    successors: List[str] = field(default_factory=list)

    earliest_start: float = 0.0

    earliest_finish: float = 0.0

    latest_start: float = 0.0

    latest_finish: float = 0.0

    total_float: float = 0.0

    critical: bool = False


# ============================================================

@dataclass
class TaskNetwork:
    """
    Directed graph of all project tasks.
    """

    tasks: Dict[str, TaskVertex] = field(default_factory=dict)

    def add(
        self,
        task: TaskVertex,
    ):

        self.tasks[task.id] = task

    # -------------------------------------------------------

    def get(
        self,
        task_id: str,
    ) -> Optional[TaskVertex]:

        return self.tasks.get(task_id)

    # -------------------------------------------------------

    def all_tasks(
        self,
    ) -> List[TaskVertex]:

        return list(self.tasks.values())

    # -------------------------------------------------------

    def total_tasks(
        self,
    ) -> int:

        return len(self.tasks)


# ============================================================
# Builder
# ============================================================

class TaskNetworkBuilder:
    """
    Converts ProjectGraph

            ↓

    Directed Task Network
    """

    def build(
        self,
        graph: ProjectGraph,
    ) -> TaskNetwork:

        network = TaskNetwork()

        #
        # name -> list(task ids)
        #
        lookup: Dict[str, List[str]] = {}

        # ----------------------------------------------------
        # Create vertices
        # ----------------------------------------------------

        for node in graph.by_type("task"):

            duration = self._parse_duration(
                node.properties.get("duration")
            )

            vertex = TaskVertex(

                id=node.id,

                name=node.name,

                duration=duration,

                planned_start=node.properties.get(
                    "planned_start"
                ),

                planned_end=node.properties.get(
                    "planned_end"
                ),

                owner=node.properties.get(
                    "owner"
                ),

                status=node.properties.get(
                    "status"
                ),

                progress=float(
                    node.properties.get(
                        "progress",
                        0,
                    )
                    or 0
                ),

                schedule_health=node.properties.get(
                    "schedule_health"
                ),
            )

            network.add(vertex)

            key = node.name.strip().lower()

            lookup.setdefault(
                key,
                []
            ).append(node.id)
                # ----------------------------------------------------
        # Build predecessor/successor relationships
        # ----------------------------------------------------

        for node in graph.by_type("task"):

            current = network.get(node.id)

            if current is None:
                continue

            dependencies = node.properties.get(
                "dependencies",
                [],
            )

            if dependencies is None:
                dependencies = []

            if not isinstance(
                dependencies,
                list,
            ):
                dependencies = [dependencies]

            for dependency in dependencies:

                dependency_name = (
                    str(dependency)
                    .strip()
                    .lower()
                )

                if not dependency_name:
                    continue

                #
                # Lookup predecessor
                #
                matches = lookup.get(
                    dependency_name
                )

                #
                # Dependency not found
                #
                if not matches:
                    continue

                #
                # If duplicate task names exist,
                # use the first one for now.
                #
                predecessor_id = matches[0]

                #
                # Avoid self dependency
                #
                if predecessor_id == current.id:
                    continue

                #
                # Prevent duplicates
                #
                if predecessor_id not in current.predecessors:

                    current.predecessors.append(
                        predecessor_id
                    )

                predecessor = network.get(
                    predecessor_id
                )

                if predecessor is None:
                    continue

                if current.id not in predecessor.successors:

                    predecessor.successors.append(
                        current.id
                    )

        return network

    # ========================================================

    @staticmethod
    def _parse_duration(
        value,
    ) -> float:

        """
        Converts

            5
            5.0
            "5"
            "5d"
            "5 days"

        into

            5.0
        """

        if value is None:
            return 0.0

        if isinstance(
            value,
            (int, float),
        ):
            return float(value)

        text = (
            str(value)
            .lower()
            .replace("days", "")
            .replace("day", "")
            .replace("d", "")
            .strip()
        )

        try:
            return float(text)
        except Exception:
            return 0.0
            # ========================================================
    # Utility Methods
    # ========================================================

    @staticmethod
    def find_start_tasks(
        network: TaskNetwork,
    ) -> List[TaskVertex]:
        """
        Tasks having no predecessors.
        """

        return [

            task

            for task in network.all_tasks()

            if len(task.predecessors) == 0

        ]

    # --------------------------------------------------------

    @staticmethod
    def find_end_tasks(
        network: TaskNetwork,
    ) -> List[TaskVertex]:
        """
        Tasks having no successors.
        """

        return [

            task

            for task in network.all_tasks()

            if len(task.successors) == 0

        ]

    # --------------------------------------------------------

    @staticmethod
    def statistics(
        network: TaskNetwork,
    ) -> Dict[str, int]:

        total_edges = 0

        isolated = 0

        for task in network.all_tasks():

            total_edges += len(
                task.successors
            )

            if (
                len(task.predecessors) == 0
                and
                len(task.successors) == 0
            ):
                isolated += 1

        return {

            "total_tasks": network.total_tasks(),

            "start_tasks": len(
                TaskNetworkBuilder.find_start_tasks(
                    network
                )
            ),

            "end_tasks": len(
                TaskNetworkBuilder.find_end_tasks(
                    network
                )
            ),

            "isolated_tasks": isolated,

            "dependency_edges": total_edges,
        }

    # --------------------------------------------------------

    @staticmethod
    def print_network(
        network: TaskNetwork,
    ) -> None:

        print()

        print("=" * 80)

        print("TASK NETWORK")

        print("=" * 80)

        stats = TaskNetworkBuilder.statistics(
            network
        )

        print()

        for key, value in stats.items():

            print(
                f"{key:<20}: {value}"
            )

        print()

        print("=" * 80)

        for task in network.all_tasks():

            print()

            print(f"Task : {task.name}")

            print(f"ID   : {task.id}")

            print(
                f"Duration : {task.duration}"
            )

            print(
                f"Status   : {task.status}"
            )

            print(
                f"Progress : {task.progress}"
            )

            print(
                "Predecessors:",
                len(task.predecessors),
            )

            if task.predecessors:

                for predecessor in task.predecessors:

                    print(
                        "   <-",
                        predecessor,
                    )

            print(
                "Successors:",
                len(task.successors),
            )

            if task.successors:

                for successor in task.successors:

                    print(
                        "   ->",
                        successor,
                    )

            print("-" * 80)