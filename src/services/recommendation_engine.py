from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from src.services.schedule_engine import ScheduleMetrics
from src.services.dependency_engine import DependencyReport
from src.services.risk_engine import RiskReport, RiskLevel
from src.services.health_score_engine import HealthScore
from src.services.forecast_engine import Forecast
from src.services.critical_path_engine import CriticalPathResult


# ============================================================
# Priority
# ============================================================

class RecommendationPriority(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


# ============================================================
# Recommendation
# ============================================================

@dataclass
class Recommendation:

    title: str

    description: str

    priority: RecommendationPriority

    category: str

    expected_impact: str


# ============================================================
# Report
# ============================================================

@dataclass
class RecommendationReport:

    recommendations: List[Recommendation] = field(
        default_factory=list
    )

    @property
    def total(self):

        return len(self.recommendations)


# ============================================================
# Engine
# ============================================================

class RecommendationEngine:

    """
    Generates actionable project recommendations
    using analytics from all engines.
    """

    def analyze(

        self,

        schedule: ScheduleMetrics,

        dependency: DependencyReport,

        risk: RiskReport,

        health: HealthScore,

        forecast: Forecast,

        critical: CriticalPathResult,

    ) -> RecommendationReport:

        report = RecommendationReport()

        # =====================================================
        # Health Recommendations
        # =====================================================

        if health.overall_score < 60:

            report.recommendations.append(

                Recommendation(

                    title="Project Health Recovery",

                    description=(
                        "Project health is below acceptable "
                        "threshold. Initiate recovery planning."
                    ),

                    priority=RecommendationPriority.CRITICAL,

                    category="Health",

                    expected_impact="Improve overall project stability.",
                )
            )

        # =====================================================
        # Schedule Recommendations
        # =====================================================

        if schedule.delayed_tasks > 0:

            report.recommendations.append(

                Recommendation(

                    title="Recover Delayed Tasks",

                    description=(
                        f"{schedule.delayed_tasks} tasks are delayed. "
                        "Prioritize recovery actions."
                    ),

                    priority=RecommendationPriority.HIGH,

                    category="Schedule",

                    expected_impact="Reduce project delay.",
                )
            )

        if forecast.delay_probability > 60:

            report.recommendations.append(

                Recommendation(

                    title="Mitigate Delivery Risk",

                    description=(
                        "Forecast indicates a high probability "
                        "of schedule slippage."
                    ),

                    priority=RecommendationPriority.CRITICAL,

                    category="Forecast",

                    expected_impact="Increase delivery confidence.",
                )
            )

        # =====================================================
        # Dependency Recommendations
        # =====================================================

        if dependency.circular_dependencies:

            report.recommendations.append(

                Recommendation(

                    title="Resolve Circular Dependencies",

                    description=(
                        "Circular task dependencies detected."
                    ),

                    priority=RecommendationPriority.CRITICAL,

                    category="Dependencies",

                    expected_impact="Prevent scheduling deadlocks.",
                )
            )

        if dependency.missing_dependencies:

            report.recommendations.append(

                Recommendation(

                    title="Repair Missing Dependencies",

                    description=(
                        "Some predecessor tasks are missing."
                    ),

                    priority=RecommendationPriority.HIGH,

                    category="Dependencies",

                    expected_impact="Improve schedule integrity.",
                )
            )

        # =====================================================
        # Risk Recommendations
        # =====================================================

        if risk.critical > 0:

            report.recommendations.append(

                Recommendation(

                    title="Escalate Critical Risks",

                    description=(
                        "Critical project risks require "
                        "executive attention."
                    ),

                    priority=RecommendationPriority.CRITICAL,

                    category="Risk",

                    expected_impact="Reduce project failure risk.",
                )
            )

        if risk.high > 5:

            report.recommendations.append(

                Recommendation(

                    title="Conduct Risk Review",

                    description=(
                        "Large number of high-severity risks detected."
                    ),

                    priority=RecommendationPriority.HIGH,

                    category="Risk",

                    expected_impact="Improve project resilience.",
                )
            )

        # =====================================================
        # Critical Path Recommendation
        # =====================================================

        if len(critical.critical_path) > 20:

            report.recommendations.append(

                Recommendation(

                    title="Reduce Critical Path Length",

                    description=(
                        "Critical path is unusually long. "
                        "Consider parallel execution."
                    ),

                    priority=RecommendationPriority.HIGH,

                    category="Critical Path",

                    expected_impact="Reduce overall project duration.",
                )
            )

        # =====================================================
        # Sort by Priority
        # =====================================================

        priority_order = {

            RecommendationPriority.CRITICAL: 0,

            RecommendationPriority.HIGH: 1,

            RecommendationPriority.MEDIUM: 2,

            RecommendationPriority.LOW: 3,
        }

        report.recommendations.sort(

            key=lambda recommendation: (
                priority_order[
                    recommendation.priority
                ],
                recommendation.title,
            )
        )

        return report

    # =====================================================
    # Report
    # =====================================================

    @staticmethod
    def print_report(
        report: RecommendationReport,
    ) -> None:

        print()

        print("=" * 90)

        print("PROJECT RECOMMENDATIONS")

        print("=" * 90)

        print()

        for index, recommendation in enumerate(

            report.recommendations,

            start=1,

        ):

            print(
                f"{index}. [{recommendation.priority}] "
                f"{recommendation.title}"
            )

            print(
                f"   Category : {recommendation.category}"
            )

            print(
                f"   Action   : {recommendation.description}"
            )

            print(
                f"   Impact   : {recommendation.expected_impact}"
            )

            print()

        print("=" * 90)