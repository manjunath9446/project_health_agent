from __future__ import annotations

from typing import Optional

from loguru import logger

from src.core.ai_orchestrator import AIOrchestrator
from src.schemas.project_context import ProjectContext


class AIRuntimeService:
    """
    Singleton runtime used by the API.

    Responsibilities

        • Own AI Orchestrator

        • Load ProjectContext

        • Answer questions

        • Execute simulations

    """

    def __init__(self):

        self.orchestrator = AIOrchestrator()

        self.loaded = False

    # =====================================================

    def load_project(

        self,

        context: ProjectContext,

    ):

        logger.info(
            "Loading project into AI runtime."
        )

        self.orchestrator.load_project(
            context
        )

        self.loaded = True

    # =====================================================

    async def ask(

        self,

        question: str,

    ) -> str:

        if not self.loaded:

            raise RuntimeError(
                "No project loaded."
            )

        return await self.orchestrator.ask(
            question
        )

    # =====================================================

    def simulate(

        self,

        task: str,

        duration: float,

    ):

        if not self.loaded:

            raise RuntimeError(
                "No project loaded."
            )

        return self.orchestrator.simulate(

            task,

            duration,

        )
        # =====================================================

    def blackboard(self):

        return self.orchestrator.blackboard_snapshot()

    # =====================================================

    def memory(self):

        return self.orchestrator.memory_stats()

    # =====================================================

    def executive_summary(self):

        return self.orchestrator.blackboard.get(

            "executive_summary"

        )

    # =====================================================

    def recommendations(self):

        return self.orchestrator.blackboard.get(

            "recommendations"

        )

    # =====================================================

    def forecast(self):

        return self.orchestrator.blackboard.get(

            "forecast"

        )

    # =====================================================

    def health(self):

        return self.orchestrator.blackboard.get(

            "health_score"

        )

    # =====================================================

    def reset(self):

        logger.info(
            "Resetting AI Runtime."
        )

        self.orchestrator.blackboard.clear()

        self.loaded = False


#
# Global Runtime
#

ai_runtime = AIRuntimeService()