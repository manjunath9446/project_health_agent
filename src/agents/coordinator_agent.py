from __future__ import annotations

from loguru import logger

from src.core.blackboard import Blackboard

from src.agents.analytics_agent import AnalyticsAgent
from src.agents.executive_summary_agent import ExecutiveSummaryAgent


class CoordinatorAgent:
    """
    Central orchestrator for the AI platform.

    Responsibilities

        • Own the Blackboard

        • Execute all agents

        • Maintain execution order

        • Return final results
    """

    def __init__(self):

        self.blackboard = Blackboard()

        self.analytics_agent = AnalyticsAgent(
            self.blackboard
        )

        self.executive_agent = ExecutiveSummaryAgent(
            self.blackboard
        )

    # ======================================================

    def load_project(
        self,
        project_context,
    ):

        self.blackboard.put(

            key="project_context",

            value=project_context,

            producer="CoordinatorAgent",

        )

        logger.info(
            "ProjectContext loaded into Blackboard."
        )

    # ======================================================
    # Run Pipeline
    # ======================================================

    def run(self):

        logger.info(
            "CoordinatorAgent started."
        )

        #
        # Ensure ProjectContext exists
        #

        if not self.blackboard.exists(
            "project_context"
        ):

            raise ValueError(
                "ProjectContext not loaded."
            )

        # ==================================================
        # Analytics
        # ==================================================

        logger.info(
            "Running AnalyticsAgent..."
        )

        self.analytics_agent.run()

        logger.success(
            "AnalyticsAgent completed."
        )

        # ==================================================
        # Executive Summary
        # ==================================================

        logger.info(
            "Running ExecutiveSummaryAgent..."
        )

        self.executive_agent.run()

        logger.success(
            "ExecutiveSummaryAgent completed."
        )

        logger.success(
            "Coordinator pipeline finished."
        )

        return self.results()

    # ======================================================
    # Results
    # ======================================================

    def results(self):

        return {

            "project_context": self.blackboard.get(
                "project_context"
            ),

            "project_graph": self.blackboard.get(
                "project_graph"
            ),

            "task_network": self.blackboard.get(
                "task_network"
            ),

            "schedule_metrics": self.blackboard.get(
                "schedule_metrics"
            ),

            "dependency_report": self.blackboard.get(
                "dependency_report"
            ),

            "critical_path": self.blackboard.get(
                "critical_path"
            ),

            "risk_report": self.blackboard.get(
                "risk_report"
            ),

            "health_score": self.blackboard.get(
                "health_score"
            ),

            "forecast": self.blackboard.get(
                "forecast"
            ),

            "recommendations": self.blackboard.get(
                "recommendations"
            ),

            "executive_summary": self.blackboard.get(
                "executive_summary"
            ),
        }

    # ======================================================
    # Blackboard Access
    # ======================================================

    def get_blackboard(self) -> Blackboard:

        return self.blackboard
        # ======================================================
    # Reset Blackboard
    # ======================================================

    def reset(self):

        logger.info(
            "Resetting CoordinatorAgent."
        )

        self.blackboard.clear()

    # ======================================================
    # Status
    # ======================================================

    def print_pipeline_status(self):

        print()

        print("=" * 80)

        print("COORDINATOR AGENT")

        print("=" * 80)

        status = {

            "Project Context":
                self.blackboard.exists(
                    "project_context"
                ),

            "Project Graph":
                self.blackboard.exists(
                    "project_graph"
                ),

            "Task Network":
                self.blackboard.exists(
                    "task_network"
                ),

            "Schedule Metrics":
                self.blackboard.exists(
                    "schedule_metrics"
                ),

            "Dependency Report":
                self.blackboard.exists(
                    "dependency_report"
                ),

            "Critical Path":
                self.blackboard.exists(
                    "critical_path"
                ),

            "Risk Report":
                self.blackboard.exists(
                    "risk_report"
                ),

            "Health Score":
                self.blackboard.exists(
                    "health_score"
                ),

            "Forecast":
                self.blackboard.exists(
                    "forecast"
                ),

            "Recommendations":
                self.blackboard.exists(
                    "recommendations"
                ),

            "Executive Summary":
                self.blackboard.exists(
                    "executive_summary"
                ),
        }

        for key, value in status.items():

            print(

                f"{key:25}",

                "✓" if value else "✗",

            )

        print()

        print("=" * 80)

    # ======================================================
    # Blackboard Viewer
    # ======================================================

    def print_blackboard(self):

        self.blackboard.print_board()

    # ======================================================
    # Snapshot
    # ======================================================

    def snapshot(self):

        return self.blackboard.snapshot()