from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from typing import Dict, List

from src.services.task_network_builder import (
    TaskNetwork,
    TaskVertex,
)


# ============================================================
# Result
# ============================================================

@dataclass
class CriticalPathResult:

    project_duration: float = 0

    critical_tasks: List[str] = field(default_factory=list)

    critical_path: List[TaskVertex] = field(default_factory=list)


# ============================================================
# Engine
# ============================================================

class CriticalPathEngine:
    """
    Computes

    • Earliest Start

    • Earliest Finish

    • Latest Start

    • Latest Finish

    • Float

    • Critical Path
    """

    # -------------------------------------------------------

    def analyze(
        self,
        network: TaskNetwork,
    ) -> CriticalPathResult:

        #
        # Forward pass
        #

        self._forward_pass(network)

        #
        # Backward pass
        #

        self._backward_pass(network)

        #
        # Float
        #

        self._calculate_float(network)

        #
        # Build Result
        #

        result = CriticalPathResult()

        result.project_duration = max(

            task.earliest_finish

            for task in network.all_tasks()

        )

        for task in network.all_tasks():

            if task.critical:

                result.critical_tasks.append(
                    task.id
                )

                result.critical_path.append(
                    task
                )

        result.critical_path.sort(

            key=lambda t: t.earliest_start

        )

        return result

    # =========================================================
    # Forward Pass
    # =========================================================

    def _forward_pass(
        self,
        network: TaskNetwork,
    ) -> None:
        """
        Computes

            Earliest Start (ES)

            Earliest Finish (EF)
        """

        #
        # Calculate in-degree
        #

        indegree: Dict[str, int] = {}

        for task in network.all_tasks():

            indegree[task.id] = len(
                task.predecessors
            )

        #
        # Queue of start tasks
        #

        queue = deque()

        for task in network.all_tasks():

            if indegree[task.id] == 0:

                queue.append(task.id)

                task.earliest_start = 0

                task.earliest_finish = task.duration

        #
        # Topological traversal
        #

        while queue:

            current_id = queue.popleft()

            current = network.get(current_id)

            if current is None:
                continue

            for successor_id in current.successors:

                successor = network.get(
                    successor_id
                )

                if successor is None:
                    continue

                #
                # Successor ES
                #

                successor.earliest_start = max(

                    successor.earliest_start,

                    current.earliest_finish,

                )

                successor.earliest_finish = (

                    successor.earliest_start
                    +
                    successor.duration

                )

                indegree[successor.id] -= 1

                if indegree[successor.id] == 0:

                    queue.append(
                        successor.id
                    )

    # =========================================================
    # Backward Pass
    # =========================================================

    def _backward_pass(
        self,
        network: TaskNetwork,
    ) -> None:
        """
        Computes

            Latest Finish (LF)

            Latest Start (LS)
        """

        #
        # Project duration
        #

        project_finish = max(
            task.earliest_finish
            for task in network.all_tasks()
        )

        #
        # Out-degree
        #

        outdegree: Dict[str, int] = {}

        for task in network.all_tasks():

            outdegree[task.id] = len(
                task.successors
            )

        #
        # Queue of end tasks
        #

        queue = deque()

        for task in network.all_tasks():

            if outdegree[task.id] == 0:

                task.latest_finish = project_finish

                task.latest_start = (

                    project_finish
                    - task.duration

                )

                queue.append(task.id)

        #
        # Reverse topological traversal
        #

        while queue:

            current_id = queue.popleft()

            current = network.get(current_id)

            if current is None:
                continue

            for predecessor_id in current.predecessors:

                predecessor = network.get(
                    predecessor_id
                )

                if predecessor is None:
                    continue

                #
                # First visit
                #

                if predecessor.latest_finish == 0:

                    predecessor.latest_finish = (
                        current.latest_start
                    )

                #
                # Keep smallest LF
                #

                predecessor.latest_finish = min(

                    predecessor.latest_finish,

                    current.latest_start,

                )

                predecessor.latest_start = (

                    predecessor.latest_finish
                    - predecessor.duration

                )

                outdegree[predecessor.id] -= 1

                if outdegree[predecessor.id] == 0:

                    queue.append(
                        predecessor.id
                    )

        # =========================================================
    # Float Calculation
    # =========================================================

    def _calculate_float(
        self,
        network: TaskNetwork,
    ) -> None:
        """
        Calculates

            Total Float

        and marks critical tasks.
        """

        for task in network.all_tasks():

            task.total_float = (

                task.latest_start
                -
                task.earliest_start

            )

            #
            # Allow tiny floating-point tolerance
            #

            task.critical = abs(task.total_float) < 1e-6

    # =========================================================
    # Utility
    # =========================================================

    @staticmethod
    def critical_tasks(
        network: TaskNetwork,
    ) -> List[TaskVertex]:

        return [

            task

            for task in network.all_tasks()

            if task.critical

        ]

    # ---------------------------------------------------------

    @staticmethod
    def print_report(
        result: CriticalPathResult,
    ) -> None:

        print()

        print("=" * 80)

        print("CRITICAL PATH REPORT")

        print("=" * 80)

        print()

        print(
            "Project Duration :",
            result.project_duration,
            "days",
        )

        print()

        print(
            "Critical Tasks :",
            len(result.critical_path),
        )

        print()

        print("-" * 80)

        for i, task in enumerate(
            result.critical_path,
            start=1,
        ):

            print(
                f"{i:02d}. {task.name}"
            )

            print(
                f"    ES : {task.earliest_start}"
            )

            print(
                f"    EF : {task.earliest_finish}"
            )

            print(
                f"    LS : {task.latest_start}"
            )

            print(
                f"    LF : {task.latest_finish}"
            )

            print(
                f"    Float : {task.total_float}"
            )

            print()

        print("=" * 80)