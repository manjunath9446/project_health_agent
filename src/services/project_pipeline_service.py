from __future__ import annotations

from typing import Dict, Any

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.ingestion_service import IngestionService
from src.services.project_analysis_service import ProjectAnalysisService
from src.core.ai_orchestrator import AIOrchestrator


class ProjectPipelineService:
    """
    Complete end-to-end project pipeline.

    Excel
        ↓
    Ingestion
        ↓
    AI Analytics
        ↓
    Executive Summary
        ↓
    Dashboard Data
    """

    def __init__(
        self,
        session: AsyncSession,
    ):

        self.session = session

        self.ingestion = IngestionService(session)

        self.ai = AIOrchestrator()

    # =====================================================
    # Execute Complete Pipeline
    # =====================================================

    async def process_project(
        self,
        file_path: str,
        project_name: str,
    ) -> Dict[str, Any]:

        logger.info("Starting project pipeline.")

        # -------------------------------------------------
        # STEP 1 : INGESTION
        # -------------------------------------------------

        project_id, context = await self.ingestion.ingest(
            file_path=file_path,
            project_name=project_name,
        )

        # -------------------------------------------------
        # STEP 2 : AI ANALYSIS
        # -------------------------------------------------

        self.ai.load_project(context)

        # -------------------------------------------------
        # STEP 3 : SNAPSHOT
        # -------------------------------------------------

        snapshot = self.ai.blackboard_snapshot()

        logger.success("Pipeline completed.")

        # -------------------------------------------------
        # STEP 4 : RESPONSE
        # -------------------------------------------------

        response = {

            "project_id": project_id,

            "project_name": context.project_name,

            "project_manager": context.project_manager,

            "category": context.category,

            "dashboard": snapshot,

            "executive_summary": self.ai.blackboard.get(
                "executive_summary"
            ),

            "recommendations": self.ai.blackboard.get(
                "recommendations"
            ),

            "forecast": self.ai.blackboard.get(
                "forecast"
            ),

            "health": self.ai.blackboard.get(
                "health_score"
            ),

            "risk_report": self.ai.blackboard.get(
                "risk_report"
            ),

            "root_cause": self.ai.blackboard.get(
                "root_cause_report"
            ),

        }

        # -------------------------------------------------
        # STEP 5 : SAVE AI ANALYSIS
        # -------------------------------------------------

        analysis_service = ProjectAnalysisService(
            self.session
        )

        await analysis_service.save(
            project_id=project_id,
            analysis=response,
        )

        # -------------------------------------------------
        # STEP 6 : RETURN
        # -------------------------------------------------

        return response

    # =====================================================
    # Ask AI
    # =====================================================

    async def ask(
        self,
        question: str,
    ) -> str:

        return await self.ai.ask(question)

    # =====================================================
    # Simulation
    # =====================================================

    def simulate(
        self,
        task_name: str,
        duration: float,
    ):

        return self.ai.simulate(
            task_name,
            duration,
        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.ai.blackboard.clear()

    # =====================================================
    # Status
    # =====================================================

    def status(self):

        return {

            "memory": self.ai.memory_stats(),

            "blackboard": self.ai.blackboard_snapshot(),

        }