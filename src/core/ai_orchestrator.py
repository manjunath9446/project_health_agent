from __future__ import annotations

from loguru import logger

from src.core.blackboard import Blackboard
from src.core.event_bus import EventBus

from src.services.memory_service import MemoryService
from src.services.llm_service import LLMService

from src.agents.analytics_agent import AnalyticsAgent
from src.agents.executive_summary_agent import ExecutiveSummaryAgent
from src.agents.project_qa_agent import ProjectQAAgent
from src.agents.root_cause_agent import RootCauseAgent
from src.agents.what_if_simulation_agent import WhatIfSimulationAgent


class AIOrchestrator:
    """
    Enterprise AI Runtime.

    Owns

        Blackboard
        EventBus
        Memory
        LLM

    Coordinates every AI agent.
    """

    def __init__(self):

        self.blackboard = Blackboard()

        self.events = EventBus()

        self.memory = MemoryService()

        self.llm = LLMService()

        # -------------------------------
        # Agents
        # -------------------------------

        self.analytics = AnalyticsAgent(
            self.blackboard
        )

        self.executive = ExecutiveSummaryAgent(
            self.blackboard
        )

        self.qa = ProjectQAAgent(
            self.blackboard
        )

        self.root_cause = RootCauseAgent(
            self.blackboard
        )

        self.simulation = WhatIfSimulationAgent(
            self.blackboard
        )

        self._register_events()

    # =====================================================

    def _register_events(self):

        self.events.subscribe(

            "project_loaded",

            self._on_project_loaded,

        )

        self.events.subscribe(

            "analytics_completed",

            self._on_analytics_completed,

        )

        self.events.subscribe(

            "summary_completed",

            self._on_summary_completed,

        )

    # =====================================================

    def load_project(

        self,

        project_context,

    ):

        logger.info(
            "Loading project..."
        )

        self.blackboard.put(

            key="project_context",

            value=project_context,

            producer="AIOrchestrator",

        )

        self.events.publish(

            "project_loaded"

        )

    # =====================================================
    # Event Handlers
    # =====================================================

    def _on_project_loaded(self, event):

        logger.info(
            "Running analytics..."
        )

        self.analytics.run()

        self.events.publish(

            "analytics_completed"

        )

    # =====================================================

    def _on_analytics_completed(self, event):

        logger.info(
            "Generating executive summary..."
        )

        self.executive.run()

        self.root_cause.run()

        self.events.publish(

            "summary_completed"

        )

    # =====================================================

    def _on_summary_completed(self, event):

        summary = self.blackboard.get(
            "executive_summary"
        )

        self.memory.add(

            source="ExecutiveSummaryAgent",

            category="summary",

            content=str(summary),

        )

        logger.success(
            "AI pipeline completed."
        )

    # =====================================================

    async def ask(

        self,

        question: str,

    ) -> str:

        #
        # Save user question
        #

        self.memory.add(

            source="User",

            category="question",

            content=question,

        )

        answer = await self.qa.ask_llm(

            question,

            self.llm,

        )

        self.memory.add(

            source="Assistant",

            category="answer",

            content=answer,

        )

        return answer

    # =====================================================

    def simulate(

        self,

        task,
        duration,
    ):

        return self.simulation.simulate_duration_change(

            task,

            duration,

        )

    # =====================================================

    def blackboard_snapshot(self):

        return self.blackboard.snapshot()

    # =====================================================

    def memory_stats(self):

        return self.memory.stats()