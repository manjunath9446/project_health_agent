from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional

from src.services.schedule_engine import ScheduleMetrics
from src.services.critical_path_engine import CriticalPathResult
from src.services.risk_engine import RiskReport
from src.services.task_network_builder import TaskNetwork


# ============================================================
# Forecast Models
# ============================================================

@dataclass
class Forecast:

    predicted_completion: Optional[date] = None

    estimated_delay_days: int = 0

    delay_probability: float = 0.0

    schedule_performance_index: float = 0.0

    execution_velocity: float = 0.0

    remaining_tasks: int = 0

    projected_remaining_days: int = 0

    confidence: float = 0.0

    assumptions: List[str] = field(default_factory=list)


# ============================================================
# Forecast Engine
# ============================================================

class ForecastEngine:
    """
    Predictive schedule forecasting.

    Computes

    • Estimated completion date

    • Delay probability

    • SPI

    • Remaining duration

    • Execution velocity

    """

    def analyze(

        self,

        network: TaskNetwork,

        schedule: ScheduleMetrics,

        critical: CriticalPathResult,

        risk: RiskReport,

    ) -> Forecast:

        forecast = Forecast()

        today = date.today()

        # =====================================================
        # Remaining Tasks
        # =====================================================

        forecast.remaining_tasks = max(

            schedule.total_tasks
            -
            schedule.completed_tasks,

            0,

        )

        # =====================================================
        # Execution Velocity
        # =====================================================

        if critical.project_duration > 0:

            forecast.execution_velocity = round(

                schedule.completed_tasks
                /
                critical.project_duration,

                2,

            )

        else:

            forecast.execution_velocity = 0.0

        # =====================================================
        # Schedule Performance Index (SPI)
        # =====================================================

        planned_progress = 100.0

        actual_progress = schedule.average_progress

        if planned_progress > 0:

            forecast.schedule_performance_index = round(

                actual_progress
                /
                planned_progress,

                2,

            )

        else:

            forecast.schedule_performance_index = 0.0

        # =====================================================
        # Remaining Duration
        # =====================================================

        if forecast.execution_velocity > 0:

            forecast.projected_remaining_days = int(

                forecast.remaining_tasks
                /
                forecast.execution_velocity

            )

        else:

            forecast.projected_remaining_days = 0

        # =====================================================
        # Predicted Completion Date
        # =====================================================

        forecast.predicted_completion = (

            today
            +
            timedelta(
                days=forecast.projected_remaining_days
            )

        )

        # =====================================================
        # Delay Probability
        # =====================================================

        probability = 0.0

        #
        # Risk contribution
        #

        probability += risk.critical * 12

        probability += risk.high * 6

        probability += risk.medium * 2

        #
        # Schedule Performance
        #

        if forecast.schedule_performance_index < 1:

            probability += (
                (1 - forecast.schedule_performance_index)
                * 50
            )

        #
        # Critical Path Length
        #

        probability += (
            len(critical.critical_path) * 0.30
        )

        forecast.delay_probability = round(

            min(probability, 100),

            2,

        )

        # =====================================================
        # Estimated Delay Days
        # =====================================================

        if forecast.delay_probability < 20:

            forecast.estimated_delay_days = 0

        elif forecast.delay_probability < 40:

            forecast.estimated_delay_days = 5

        elif forecast.delay_probability < 60:

            forecast.estimated_delay_days = 10

        elif forecast.delay_probability < 80:

            forecast.estimated_delay_days = 20

        else:

            forecast.estimated_delay_days = 30

        #
        # Update completion date
        #

        forecast.predicted_completion += timedelta(

            days=forecast.estimated_delay_days

        )

        # =====================================================
        # Forecast Confidence
        # =====================================================

        confidence = 100.0

        confidence -= risk.critical * 8

        confidence -= risk.high * 4

        confidence -= risk.medium * 2

        confidence -= abs(
            1 - forecast.schedule_performance_index
        ) * 30

        forecast.confidence = round(

            max(confidence, 0),

            2,

        )

        # =====================================================
        # Assumptions
        # =====================================================

        forecast.assumptions.clear()

        forecast.assumptions.append(

            "Forecast assumes current execution velocity remains constant."

        )

        forecast.assumptions.append(

            "No additional project scope is introduced."

        )

        forecast.assumptions.append(

            "Current resource allocation remains unchanged."

        )

        if risk.critical > 0:

            forecast.assumptions.append(

                "Critical risks are expected to impact delivery."
            )

        if forecast.schedule_performance_index < 1:

            forecast.assumptions.append(

                "Schedule performance remains below planned velocity."
            )

        if forecast.delay_probability > 70:

            forecast.assumptions.append(

                "Project has a high probability of schedule slippage."
            )

        return forecast

    # =====================================================
    # Report
    # =====================================================

    @staticmethod
    def print_report(
        forecast: Forecast,
    ) -> None:

        print()

        print("=" * 90)

        print("PROJECT FORECAST REPORT")

        print("=" * 90)

        print()

        print(
            f"Predicted Completion : {forecast.predicted_completion}"
        )

        print(
            f"Estimated Delay      : {forecast.estimated_delay_days} days"
        )

        print(
            f"Delay Probability    : {forecast.delay_probability:.2f}%"
        )

        print(
            f"SPI                  : {forecast.schedule_performance_index:.2f}"
        )

        print(
            f"Execution Velocity   : {forecast.execution_velocity:.2f} tasks/day"
        )

        print(
            f"Remaining Tasks      : {forecast.remaining_tasks}"
        )

        print(
            f"Remaining Duration   : {forecast.projected_remaining_days} days"
        )

        print(
            f"Forecast Confidence  : {forecast.confidence:.2f}%"
        )

        print()

        print("-" * 90)

        print("Forecast Assumptions")

        print("-" * 90)

        for assumption in forecast.assumptions:

            print(f"• {assumption}")

        print()

        print("=" * 90)