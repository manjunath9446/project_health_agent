from __future__ import annotations

import json
from typing import Any

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.project_analysis import ProjectAnalysis


class ProjectAnalysisService:
    """
    Persists the final AI analysis for a project.

    The stored analysis is later used for:

    • Weekly Reports
    • Monthly Executive Presentation
    • Portfolio Analytics
    """

    def __init__(self, session: AsyncSession):

        self.session = session

    # =====================================================
    # SAVE ANALYSIS
    # =====================================================

    async def save(
        self,
        project_id: int,
        analysis: dict[str, Any],
    ) -> ProjectAnalysis:

        health = analysis.get("health")
        forecast = analysis.get("forecast")
        risk = analysis.get("risk_report")
        recommendations = analysis.get("recommendations")
        executive_summary = analysis.get("executive_summary")

        # -------------------------------------------------
        # Determine RAG
        # -------------------------------------------------

        health_score = getattr(health, "overall_score", 0)

        delay_probability = getattr(
            forecast,
            "delay_probability",
            0,
        )

        critical_risks = getattr(
        risk,
        "critical",
        0,
        )

        high_risks = getattr(
        risk,
        "high",
        0,
                )

# ------------------------------------
# RAG Decision
# ------------------------------------

        if (
        health_score < 50
        or delay_probability >= 80
        or critical_risks >= 5
        ):

            rag = "RED"

        elif (
            health_score < 75
        or delay_probability >= 40
            or high_risks >= 10
    ):

            rag = "AMBER"

        else:

             rag = "GREEN"

        # -------------------------------------------------
        # Forecast
        # -------------------------------------------------

        forecast_delay = getattr(
            forecast,
            "estimated_delay_days",
            0,
        )

        delay_probability = getattr(
            forecast,
            "delay_probability",
            0,
        )

        # -------------------------------------------------
        # Serialize helper
        # -------------------------------------------------

        def serialize(obj: Any) -> str:

            if obj is None:
                return ""

            try:

                if hasattr(obj, "model_dump"):

                    return json.dumps(
                        obj.model_dump(),
                        indent=2,
                        default=str,
                    )

                if hasattr(obj, "dict"):

                    return json.dumps(
                        obj.dict(),
                        indent=2,
                        default=str,
                    )

                if isinstance(obj, dict):

                    return json.dumps(
                        obj,
                        indent=2,
                        default=str,
                    )

                if isinstance(obj, list):

                    data = []

                    for item in obj:

                        if hasattr(item, "model_dump"):
                            data.append(item.model_dump())

                        elif hasattr(item, "dict"):
                            data.append(item.dict())

                        else:
                            data.append(str(item))

                    return json.dumps(
                        data,
                        indent=2,
                        default=str,
                    )

                return str(obj)

            except Exception:

                return str(obj)

        # -------------------------------------------------
        # Create Row
        # -------------------------------------------------

        row = ProjectAnalysis(

            project_id=project_id,

            rag_status=rag,

            health_score=float(health_score),

            forecast_delay=int(forecast_delay),

            delay_probability=float(delay_probability),

            executive_summary=serialize(
                executive_summary
            ),

            recommendations=serialize(
                recommendations
            ),

            risks=serialize(
                risk
            ),

        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        self.session.add(row)

        await self.session.commit()

        await self.session.refresh(row)

        logger.success(
            "Saved AI analysis for Project ID {}",
            project_id,
        )

        return row

    # =====================================================
    # GET ANALYSIS
    # =====================================================

    async def get(
        self,
        project_id: int,
    ) -> ProjectAnalysis | None:

        return await self.session.get(
            ProjectAnalysis,
            project_id,
        )