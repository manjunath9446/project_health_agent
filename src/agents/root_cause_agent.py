from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from loguru import logger

from src.core.blackboard import Blackboard


# ============================================================
# Root Cause
# ============================================================

@dataclass
class RootCause:

    category: str

    severity: str

    cause: str

    evidence: str

    recommendation: str


# ============================================================
# Report
# ============================================================

@dataclass
class RootCauseReport:

    causes: List[RootCause] = field(default_factory=list)

    @property
    def total(self):

        return len(self.causes)


# ============================================================
# Agent
# ============================================================

class RootCauseAgent:

    """
    Determines WHY the project is unhealthy.

    Reads

        Health
        Risks
        Forecast
        Schedule
        Recommendations

    Produces

        root_cause_report
    """

    def __init__(
        self,
        blackboard: Blackboard,
    ):

        self.blackboard = blackboard

    # =====================================================

    def run(self):

        logger.info(
            "RootCauseAgent started."
        )

        health = self.blackboard.get(
            "health_score"
        )

        risk = self.blackboard.get(
            "risk_report"
        )

        schedule = self.blackboard.get(
            "schedule_metrics"
        )

        forecast = self.blackboard.get(
            "forecast"
        )

        dependency = self.blackboard.get(
            "dependency_report"
        )

        report = RootCauseReport()

        # -------------------------------------------------
        # Poor Health
        # -------------------------------------------------

        if health.overall_score < 60:

            report.causes.append(

                RootCause(

                    category="Health",

                    severity="Critical",

                    cause="Low overall project health.",

                    evidence=(
                        f"Health Score = "
                        f"{health.overall_score:.2f}%"
                    ),

                    recommendation=(
                        "Review project execution immediately."
                    ),

                )

            )

        # -------------------------------------------------
        # Delayed Schedule
        # -------------------------------------------------

        if schedule.delayed_tasks > 0:

            report.causes.append(

                RootCause(

                    category="Schedule",

                    severity="High",

                    cause="Multiple delayed tasks.",

                    evidence=(
                        f"{schedule.delayed_tasks} delayed tasks."
                    ),

                    recommendation=(
                        "Recover delayed activities."
                    ),

                )

            )

        # -------------------------------------------------
        # High Delay Probability
        # -------------------------------------------------

        if forecast.delay_probability > 60:

            report.causes.append(

                RootCause(

                    category="Forecast",

                    severity="High",

                    cause="High probability of schedule slippage.",

                    evidence=(
                        f"{forecast.delay_probability:.1f}%"
                    ),

                    recommendation=(
                        "Accelerate critical work."
                    ),

                )

            )

        # -------------------------------------------------
        # Risks
        # -------------------------------------------------

        if risk.critical > 0:

            report.causes.append(

                RootCause(

                    category="Risk",

                    severity="Critical",

                    cause="Critical project risks detected.",

                    evidence=(
                        f"{risk.critical} critical risks."
                    ),

                    recommendation=(
                        "Mitigate critical risks immediately."
                    ),

                )

            )

        elif risk.high > 0:

            report.causes.append(

                RootCause(

                    category="Risk",

                    severity="High",

                    cause="High severity risks impacting execution.",

                    evidence=(
                        f"{risk.high} high risks."
                    ),

                    recommendation=(
                        "Review mitigation plans."
                    ),

                )

            )

        # -------------------------------------------------
        # Dependency Problems
        # -------------------------------------------------

        if dependency.circular_dependencies:

            report.causes.append(

                RootCause(

                    category="Dependencies",

                    severity="Critical",

                    cause="Circular task dependencies detected.",

                    evidence=(
                        f"{len(dependency.circular_dependencies)} circular dependencies."
                    ),

                    recommendation=(
                        "Resolve dependency cycles."
                    ),

                )

            )

        if dependency.missing_dependencies:

            report.causes.append(

                RootCause(

                    category="Dependencies",

                    severity="Medium",

                    cause="Missing predecessor tasks.",

                    evidence=(
                        f"{len(dependency.missing_dependencies)} missing dependencies."
                    ),

                    recommendation=(
                        "Repair dependency links."
                    ),

                )

            )

        # -------------------------------------------------
        # Sort by Severity
        # -------------------------------------------------

        priority = {

            "Critical": 0,

            "High": 1,

            "Medium": 2,

            "Low": 3,

        }

        report.causes.sort(

            key=lambda cause: (
                priority.get(
                    cause.severity,
                    99,
                ),
                cause.category,
            )

        )

        # -------------------------------------------------
        # Store on Blackboard
        # -------------------------------------------------

        self.blackboard.put(

            key="root_cause_report",

            value=report,

            producer="RootCauseAgent",

        )

        logger.success(
            "Root cause analysis completed."
        )

        return report

    # =====================================================
    # Report
    # =====================================================

    @staticmethod
    def print_report(
        report: RootCauseReport,
    ) -> None:

        print()

        print("=" * 90)

        print("ROOT CAUSE ANALYSIS")

        print("=" * 90)

        print()

        print(
            f"Total Causes : {report.total}"
        )

        print()

        for index, cause in enumerate(
            report.causes,
            start=1,
        ):

            print(
                f"{index}. [{cause.severity}] {cause.category}"
            )

            print(
                f"   Cause : {cause.cause}"
            )

            print(
                f"   Evidence : {cause.evidence}"
            )

            print(
                f"   Recommendation : {cause.recommendation}"
            )

            print()

        print("=" * 90)