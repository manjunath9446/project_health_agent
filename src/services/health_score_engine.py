from __future__ import annotations

from dataclasses import dataclass

from src.services.schedule_engine import ScheduleMetrics
from src.services.dependency_engine import DependencyReport
from src.services.risk_engine import RiskReport
from src.services.critical_path_engine import CriticalPathResult


# ============================================================
# Health Score Model
# ============================================================

@dataclass
class HealthScore:

    schedule_score: float = 0.0

    dependency_score: float = 0.0

    execution_score: float = 0.0

    risk_score: float = 0.0

    critical_path_score: float = 0.0

    overall_score: float = 0.0

    status: str = "UNKNOWN"


# ============================================================
# Engine
# ============================================================

class HealthScoreEngine:
    """
    Computes overall project health.

    Components

        Schedule

        Dependencies

        Execution

        Risk

        Critical Path
    """

    SCHEDULE_WEIGHT = 0.30

    EXECUTION_WEIGHT = 0.25

    RISK_WEIGHT = 0.20

    DEPENDENCY_WEIGHT = 0.15

    CRITICAL_WEIGHT = 0.10

    def analyze(

        self,

        schedule: ScheduleMetrics,

        dependency: DependencyReport,

        risk: RiskReport,

        critical: CriticalPathResult,

    ) -> HealthScore:

        score = HealthScore()

        score.schedule_score = self._schedule_score(
            schedule
        )

        score.execution_score = self._execution_score(
            schedule
        )

        score.dependency_score = self._dependency_score(
            dependency
        )

        score.risk_score = self._risk_score(
            risk
        )

        score.critical_path_score = self._critical_score(
            critical
        )

        # =====================================================
        # Overall Weighted Score
        # =====================================================

        score.overall_score = round(

            (
                score.schedule_score
                * self.SCHEDULE_WEIGHT

                +

                score.execution_score
                * self.EXECUTION_WEIGHT

                +

                score.risk_score
                * self.RISK_WEIGHT

                +

                score.dependency_score
                * self.DEPENDENCY_WEIGHT

                +

                score.critical_path_score
                * self.CRITICAL_WEIGHT
            ),

            2,
        )

        #
        # Overall Status
        #

        if score.overall_score >= 90:

            score.status = "EXCELLENT"

        elif score.overall_score >= 75:

            score.status = "GOOD"

        elif score.overall_score >= 60:

            score.status = "FAIR"

        elif score.overall_score >= 40:

            score.status = "POOR"

        else:

            score.status = "CRITICAL"

        return score

    # =====================================================
    # Individual Scoring
    # =====================================================

    @staticmethod
    def _schedule_score(
        schedule: ScheduleMetrics,
    ) -> float:

        score = 100.0

        score -= schedule.delayed_tasks * 2

        score = max(score, 0)

        return round(score, 2)

    # -----------------------------------------------------

    @staticmethod
    def _execution_score(
        schedule: ScheduleMetrics,
    ) -> float:

        return round(
            schedule.completed_percentage,
            2,
        )

    # -----------------------------------------------------

    @staticmethod
    def _dependency_score(
        dependency: DependencyReport,
    ) -> float:

        score = 100.0

        score -= len(
            dependency.missing_dependencies
        ) * 5

        score -= len(
            dependency.circular_dependencies
        ) * 10

        score -= len(
            dependency.self_dependencies
        ) * 5

        score = max(score, 0)

        return round(score, 2)

    # -----------------------------------------------------

    @staticmethod
    def _risk_score(
        risk: RiskReport,
    ) -> float:

        score = 100.0

        score -= risk.critical * 15

        score -= risk.high * 8

        score -= risk.medium * 4

        score -= risk.low * 2

        score = max(score, 0)

        return round(score, 2)

    # -----------------------------------------------------

    @staticmethod
    def _critical_score(
        critical: CriticalPathResult,
    ) -> float:

        if len(critical.critical_path) == 0:
            return 100.0

        #
        # Longer critical paths generally
        # indicate higher schedule sensitivity.
        #

        score = 100.0 - len(
            critical.critical_path
        ) * 0.5

        score = max(score, 0)

        return round(score, 2)

    # =========================================================
    # Report
    # =========================================================

    @staticmethod
    def print_report(
        score: HealthScore,
    ) -> None:

        print()

        print("=" * 90)

        print("PROJECT HEALTH REPORT")

        print("=" * 90)

        print()

        print(
            f"Overall Health     : {score.overall_score:.2f}%"
        )

        print(
            f"Project Status     : {score.status}"
        )

        print()

        print("-" * 90)

        print(
            f"Schedule Score     : {score.schedule_score:.2f}%"
        )

        print(
            f"Execution Score    : {score.execution_score:.2f}%"
        )

        print(
            f"Dependency Score   : {score.dependency_score:.2f}%"
        )

        print(
            f"Risk Score         : {score.risk_score:.2f}%"
        )

        print(
            f"Critical Path Score: {score.critical_path_score:.2f}%"
        )

        print()

        print("-" * 90)

        #
        # Executive Summary
        #

        if score.overall_score >= 90:

            summary = (
                "Project is performing exceptionally well. "
                "Continue monitoring execution."
            )

        elif score.overall_score >= 75:

            summary = (
                "Project is healthy with only minor issues "
                "requiring attention."
            )

        elif score.overall_score >= 60:

            summary = (
                "Project health is acceptable, but several "
                "areas need improvement."
            )

        elif score.overall_score >= 40:

            summary = (
                "Project is at risk. Immediate corrective "
                "actions are recommended."
            )

        else:

            summary = (
                "Project is in a critical state. Executive "
                "intervention is required."
            )

        print("Executive Summary")

        print("-----------------")

        print(summary)

        print()

        #
        # Score Breakdown
        #

        print("Score Interpretation")

        print("--------------------")

        print("90-100 : Excellent")

        print("75-89  : Good")

        print("60-74  : Fair")

        print("40-59  : Poor")

        print("<40    : Critical")

        print()

        print("=" * 90)