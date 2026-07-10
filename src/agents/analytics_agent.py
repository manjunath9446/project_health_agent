from __future__ import annotations

from loguru import logger

from src.core.blackboard import Blackboard

from src.schemas.project_context import ProjectContext

from src.services.graph_builder import GraphBuilder
from src.services.schedule_engine import ScheduleEngine
from src.services.dependency_engine import DependencyEngine
from src.services.task_network_builder import TaskNetworkBuilder
from src.services.critical_path_engine import CriticalPathEngine
from src.services.risk_engine import RiskEngine
from src.services.health_score_engine import HealthScoreEngine
from src.services.forecast_engine import ForecastEngine
from src.services.recommendation_engine import RecommendationEngine


class AnalyticsAgent:
    """
    Runs the complete analytics pipeline.

    Reads:

        project_context

    Produces:

        project_graph
        task_network
        schedule_metrics
        dependency_report
        critical_path
        risk_report
        health_score
        forecast
        recommendations
    """

    def __init__(
        self,
        blackboard: Blackboard,
    ):

        self.blackboard = blackboard

        self.graph_builder = GraphBuilder()

        self.network_builder = TaskNetworkBuilder()

        self.schedule_engine = ScheduleEngine()

        self.dependency_engine = DependencyEngine()

        self.critical_engine = CriticalPathEngine()

        self.risk_engine = RiskEngine()

        self.health_engine = HealthScoreEngine()

        self.forecast_engine = ForecastEngine()

        self.recommendation_engine = RecommendationEngine()

    # ==========================================================
    # Run Analytics Pipeline
    # ==========================================================

    def run(self) -> None:

        logger.info(
            "AnalyticsAgent started."
        )

        #
        # Read Project Context
        #

        project_context: ProjectContext = self.blackboard.get(
            "project_context"
        )

        if project_context is None:

            raise ValueError(
                "project_context not found on blackboard."
            )

        # =====================================================
        # Graph
        # =====================================================

        graph = self.graph_builder.build(
            project_context
        )

        self.blackboard.put(

            key="project_graph",

            value=graph,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Project graph created."
        )

        # =====================================================
        # Task Network
        # =====================================================

        network = self.network_builder.build(
            graph
        )

        self.blackboard.put(

            key="task_network",

            value=network,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Task network created."
        )

        # =====================================================
        # Schedule Analysis
        # =====================================================

        schedule = self.schedule_engine.analyze(
            graph
        )

        self.blackboard.put(

            key="schedule_metrics",

            value=schedule,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Schedule analysis completed."
        )

        # =====================================================
        # Dependency Analysis
        # =====================================================

        dependency = self.dependency_engine.analyze(
            graph
        )

        self.blackboard.put(

            key="dependency_report",

            value=dependency,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Dependency analysis completed."
        )

        # =====================================================
        # Critical Path Analysis
        # =====================================================

        critical = self.critical_engine.analyze(
            network
        )

        self.blackboard.put(

            key="critical_path",

            value=critical,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Critical path analysis completed."
        )

        # =====================================================
        # Risk Analysis
        # =====================================================

        risk = self.risk_engine.analyze(
            graph,
            network,
            critical,
        )

        self.blackboard.put(

            key="risk_report",

            value=risk,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Risk analysis completed."
        )

        # =====================================================
        # Health Score
        # =====================================================

        health = self.health_engine.analyze(
            schedule,
            dependency,
            risk,
            critical,
        )

        self.blackboard.put(

            key="health_score",

            value=health,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Health score computed."
        )

        # =====================================================
        # Forecast
        # =====================================================

        forecast = self.forecast_engine.analyze(
            network,
            schedule,
            critical,
            risk,
        )

        self.blackboard.put(

            key="forecast",

            value=forecast,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Forecast generated."
        )

        # =====================================================
        # Recommendations
        # =====================================================

        recommendations = self.recommendation_engine.analyze(
            schedule,
            dependency,
            risk,
            health,
            forecast,
            critical,
        )

        self.blackboard.put(

            key="recommendations",

            value=recommendations,

            producer="AnalyticsAgent",
        )

        logger.info(
            "Recommendations generated."
        )

        logger.success(
            "Analytics pipeline completed successfully."
        )

    # ==========================================================
    # Summary
    # ==========================================================

    def summary(self) -> dict:

        return {

            "graph": self.blackboard.exists(
                "project_graph"
            ),

            "network": self.blackboard.exists(
                "task_network"
            ),

            "schedule": self.blackboard.exists(
                "schedule_metrics"
            ),

            "dependency": self.blackboard.exists(
                "dependency_report"
            ),

            "critical_path": self.blackboard.exists(
                "critical_path"
            ),

            "risk": self.blackboard.exists(
                "risk_report"
            ),

            "health": self.blackboard.exists(
                "health_score"
            ),

            "forecast": self.blackboard.exists(
                "forecast"
            ),

            "recommendations": self.blackboard.exists(
                "recommendations"
            ),
        }

    # ==========================================================
    # Debug
    # ==========================================================

    def print_summary(self) -> None:

        print()

        print("=" * 80)

        print("ANALYTICS AGENT")

        print("=" * 80)

        summary = self.summary()

        for key, value in summary.items():

            print(

                f"{key:20} :",

                "✓" if value else "✗"

            )

        print()

        print("=" * 80)

    # ==========================================================
    # Blackboard Viewer
    # ==========================================================

    def print_blackboard(self) -> None:

        self.blackboard.print_board()