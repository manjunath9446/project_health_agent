from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from src.schemas.project_graph import ProjectGraph
from src.services.task_network_builder import TaskNetwork
from src.services.critical_path_engine import CriticalPathResult


# ============================================================
# Risk Levels
# ============================================================

class RiskLevel(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# ============================================================
# Risk Model
# ============================================================

@dataclass
class Risk:

    task_id: str

    task_name: str

    risk_type: str

    level: RiskLevel

    message: str

    recommendation: str


# ============================================================
# Risk Report
# ============================================================

@dataclass
class RiskReport:

    risks: List[Risk] = field(default_factory=list)

    low: int = 0

    medium: int = 0

    high: int = 0

    critical: int = 0

    @property
    def total(self):

        return len(self.risks)


# ============================================================
# Engine
# ============================================================

class RiskEngine:
    """
    Detects project execution risks.

    Current Rules

        • Delayed task

        • Critical delayed task

        • On Hold

        • At Risk

        • Missing owner

        • Zero progress

        • Long duration

    """

    LONG_DURATION = 30

    def analyze(

        self,

        graph: ProjectGraph,

        network: TaskNetwork,

        critical_path: CriticalPathResult,

    ) -> RiskReport:

        report = RiskReport()

        critical_ids = {

            task.id

            for task in critical_path.critical_path

        }

        today = datetime.today().date()

        for task in network.all_tasks():

            props = graph.get(task.id).properties

            status = str(
                task.status or ""
            ).lower()

            progress = task.progress

            owner = task.owner

            planned_end = task.planned_end

            duration = task.duration

            # =================================================
            # Rule 1
            # Delayed Task
            # =================================================

            if planned_end:

                try:

                    if (
                        planned_end.date() < today
                        and status != "completed"
                    ):

                        level = RiskLevel.HIGH

                        #
                        # Critical Path Delay
                        #
                        if task.id in critical_ids:
                            level = RiskLevel.CRITICAL

                        report.risks.append(

                            Risk(

                                task_id=task.id,

                                task_name=task.name,

                                risk_type="SCHEDULE_DELAY",

                                level=level,

                                message=(
                                    "Task is past its planned "
                                    "finish date."
                                ),

                                recommendation=(
                                    "Review the schedule and "
                                    "expedite completion."
                                ),
                            )
                        )

                except Exception:
                    pass

            # =================================================
            # Rule 2
            # On Hold
            # =================================================

            if props.get("on_hold", False):

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="ON_HOLD",

                        level=RiskLevel.HIGH,

                        message="Task is currently on hold.",

                        recommendation=(
                            "Identify blockers and "
                            "resume execution."
                        ),
                    )
                )

            # =================================================
            # Rule 3
            # At Risk
            # =================================================

            if props.get("at_risk", False):

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="AT_RISK",

                        level=RiskLevel.HIGH,

                        message="Task has been marked at risk.",

                        recommendation=(
                            "Investigate the root cause "
                            "and prepare mitigation."
                        ),
                    )
                )

            # =================================================
            # Rule 4
            # Missing Owner
            # =================================================

            if owner is None or str(owner).strip() == "":

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="NO_OWNER",

                        level=RiskLevel.MEDIUM,

                        message="Task has no assigned owner.",

                        recommendation=(
                            "Assign a responsible owner."
                        ),
                    )
                )
                        # =================================================
            # Rule 5
            # Zero Progress
            # =================================================

            if (
                status != "completed"
                and progress <= 0
            ):

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="ZERO_PROGRESS",

                        level=RiskLevel.MEDIUM,

                        message=(
                            "Task has no recorded progress."
                        ),

                        recommendation=(
                            "Verify task execution and update progress."
                        ),
                    )
                )

            # =================================================
            # Rule 6
            # Long Duration Task
            # =================================================

            if duration >= self.LONG_DURATION:

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="LONG_DURATION",

                        level=RiskLevel.MEDIUM,

                        message=(
                            f"Task duration is {duration} days."
                        ),

                        recommendation=(
                            "Consider splitting the task into "
                            "smaller work packages."
                        ),
                    )
                )

            # =================================================
            # Rule 7
            # Critical Task Not Started
            # =================================================

            if (
                task.id in critical_ids
                and status == "not started"
            ):

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="CRITICAL_NOT_STARTED",

                        level=RiskLevel.CRITICAL,

                        message=(
                            "Critical path task has not started."
                        ),

                        recommendation=(
                            "Start this task immediately to avoid "
                            "project delay."
                        ),
                    )
                )

            # =================================================
            # Rule 8
            # Critical Task On Hold
            # =================================================

            if (
                task.id in critical_ids
                and props.get("on_hold", False)
            ):

                report.risks.append(

                    Risk(

                        task_id=task.id,

                        task_name=task.name,

                        risk_type="CRITICAL_ON_HOLD",

                        level=RiskLevel.CRITICAL,

                        message=(
                            "Critical path task is currently on hold."
                        ),

                        recommendation=(
                            "Resolve blockers immediately and resume work."
                        ),
                    )
                )

            # =================================================
            # Rule 9
            # Critical Task Behind Progress
            # =================================================

            if (
                task.id in critical_ids
                and progress < 50
                and status == "in progress"
            ):

                report.risks.append(

                    Risk(

                    task_id=task.id,

                    task_name=task.name,

                    risk_type="CRITICAL_SLOW_PROGRESS",

                    level=RiskLevel.HIGH,

                    message=(

                    "Critical task is progressing slower than expected."

                    ),

                    recommendation=(

                    "Increase resources or review execution plan."

                    ),
                )
                )

        # =================================================
        # Count Risk Levels
        # =================================================

        for risk in report.risks:

            if risk.level == RiskLevel.LOW:
                report.low += 1

            elif risk.level == RiskLevel.MEDIUM:
                report.medium += 1

            elif risk.level == RiskLevel.HIGH:
                report.high += 1

            elif risk.level == RiskLevel.CRITICAL:
                report.critical += 1

        # =================================================
        # Sort Risks
        # =================================================

        priority = {

            RiskLevel.CRITICAL: 0,

            RiskLevel.HIGH: 1,

            RiskLevel.MEDIUM: 2,

            RiskLevel.LOW: 3,
        }

        report.risks.sort(

            key=lambda r: (
                priority[r.level],
                r.task_name.lower(),
            )

        )

        return report

    # =========================================================
    # Utilities
    # =========================================================

    @staticmethod
    def print_report(
        report: RiskReport,
    ) -> None:

        print()

        print("=" * 90)

        print("PROJECT RISK REPORT")

        print("=" * 90)

        print()

        print(
            f"Total Risks : {report.total}"
        )

        print(
            f"Critical    : {report.critical}"
        )

        print(
            f"High        : {report.high}"
        )

        print(
            f"Medium      : {report.medium}"
        )

        print(
            f"Low         : {report.low}"
        )

        print()

        print("=" * 90)

        for index, risk in enumerate(
            report.risks,
            start=1,
        ):

            print()

            print(
                f"{index}. [{risk.level}] {risk.task_name}"
            )

            print(
                f"   Type : {risk.risk_type}"
            )

            print(
                f"   Risk : {risk.message}"
            )

            print(
                f"   Recommendation : {risk.recommendation}"
            )

        print()

        print("=" * 90)
    