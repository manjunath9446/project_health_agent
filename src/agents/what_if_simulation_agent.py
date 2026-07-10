from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import List

from loguru import logger

from src.core.blackboard import Blackboard
from src.services.task_network_builder import TaskNetworkBuilder
from src.services.critical_path_engine import CriticalPathEngine
from src.services.health_score_engine import HealthScoreEngine
from src.services.forecast_engine import ForecastEngine
from src.services.risk_engine import RiskEngine


# ============================================================
# Scenario
# ============================================================

@dataclass
class SimulationScenario:

    title: str

    description: str

    modified_tasks: List[str] = field(default_factory=list)


# ============================================================
# Result
# ============================================================

@dataclass
class SimulationResult:

    scenario: str

    old_duration: float

    new_duration: float

    duration_change: float

    old_health: float

    new_health: float

    delay_probability: float

    summary: str


# ============================================================
# Agent
# ============================================================

class WhatIfSimulationAgent:

    """
    Simulates project changes without modifying
    the original project.

    Examples

        Add Resources

        Reduce Duration

        Remove Risk

        Resolve Delay

        Parallel Execution
    """

    def __init__(
        self,
        blackboard: Blackboard,
    ):

        self.blackboard = blackboard

        self.network_builder = TaskNetworkBuilder()

        self.critical_engine = CriticalPathEngine()

        self.risk_engine = RiskEngine()

        self.health_engine = HealthScoreEngine()

        self.forecast_engine = ForecastEngine()

    # =====================================================

    def simulate_duration_change(

        self,

        task_name: str,

        new_duration: float,

    ) -> SimulationResult:

        logger.info(

            "Running duration simulation."

        )

        graph = deepcopy(

            self.blackboard.get(
                "project_graph"
            )

        )

        #
        # Modify duration
        #

        modified = False

        for task in graph.by_type("task"):

            if task.name.lower() == task_name.lower():

                task.properties[
                    "duration"
                ] = new_duration

                modified = True

                break

        if not modified:

            raise ValueError(

                f"Task '{task_name}' not found."

            )

        #
        # Rebuild network
        #

        network = self.network_builder.build(
            graph
        )

        critical = self.critical_engine.analyze(
            network
        )

        # =====================================================
        # Previous Analytics
        # =====================================================

        old_critical = self.blackboard.get(
            "critical_path"
        )

        old_health = self.blackboard.get(
            "health_score"
        )

        schedule = self.blackboard.get(
            "schedule_metrics"
        )

        dependency = self.blackboard.get(
            "dependency_report"
        )

        # =====================================================
        # Recalculate Risk
        # =====================================================

        risk = self.risk_engine.analyze(

            graph,

            network,

            critical,

        )

        # =====================================================
        # Recalculate Health
        # =====================================================

        health = self.health_engine.analyze(

            schedule,

            dependency,

            risk,

            critical,

        )

        # =====================================================
        # Recalculate Forecast
        # =====================================================

        forecast = self.forecast_engine.analyze(

            network,

            schedule,

            critical,

            risk,

        )

        # =====================================================
        # Build Result
        # =====================================================

        duration_change = (

            critical.project_duration
            -
            old_critical.project_duration

        )

        if duration_change < 0:

            summary = (

                f"Project duration improves by "

                f"{abs(duration_change)} days."

            )

        elif duration_change > 0:

            summary = (

                f"Project duration increases by "

                f"{duration_change} days."

            )

        else:

            summary = (

                "No schedule impact detected."
            )

        result = SimulationResult(

            scenario=f"Duration change: {task_name}",

            old_duration=old_critical.project_duration,

            new_duration=critical.project_duration,

            duration_change=duration_change,

            old_health=old_health.overall_score,

            new_health=health.overall_score,

            delay_probability=forecast.delay_probability,

            summary=summary,

        )

        # =====================================================
        # Store on Blackboard
        # =====================================================

        self.blackboard.put(

            key="last_simulation",

            value=result,

            producer="WhatIfSimulationAgent",

        )

        logger.success(

            "Simulation completed successfully."

        )

        return result

    # =====================================================
    # Report
    # =====================================================

    @staticmethod
    def print_report(

        result: SimulationResult,

    ):

        print()

        print("=" * 90)

        print("WHAT-IF SIMULATION")

        print("=" * 90)

        print()

        print(

            "Scenario :",

            result.scenario,

        )

        print()

        print(

            "Old Duration :", 

            result.old_duration,

            "days",

        )

        print(

            "New Duration :", 

            result.new_duration,

            "days",
        )

        print(

            "Duration Change :", 

            result.duration_change,

            "days",
        )

        print()

        print(

            "Old Health :", 

            f"{result.old_health:.2f}%",

        )

        print(

            "New Health :", 

            f"{result.new_health:.2f}%",

        )

        print()

        print(

            "Delay Probability :", 

            f"{result.delay_probability:.2f}%",

        )

        print()

        print(

            "Summary"

        )

        print(

            "-------"

        )

        print(

            result.summary

        )

        print()

        print("=" * 90)