from __future__ import annotations

from loguru import logger

from src.core.blackboard import Blackboard


class ProjectQAAgent:
    """
    Answers project questions using the Blackboard.

    Future versions can use an LLM.
    Current version answers directly from analytics.
    """

    def __init__(
        self,
        blackboard: Blackboard,
    ):

        self.blackboard = blackboard

    # =====================================================

    def ask(
        self,
        question: str,
    ) -> str:

        logger.info(
            "QA Question: {}",
            question,
        )

        q = question.lower()

        health = self.blackboard.get(
            "health_score"
        )

        risk = self.blackboard.get(
            "risk_report"
        )

        forecast = self.blackboard.get(
            "forecast"
        )

        recommendation = self.blackboard.get(
            "recommendations"
        )

        critical = self.blackboard.get(
            "critical_path"
        )

        schedule = self.blackboard.get(
            "schedule_metrics"
        )

        # ==================================================
        # Health
        # ==================================================

        if "health" in q:

            return (
                f"Overall project health is "
                f"{health.overall_score:.2f}% "
                f"({health.status})."
            )

        # ==================================================
        # Risks
        # ==================================================

        if "risk" in q:

            return (

                f"The project contains "

                f"{risk.total} risks "

                f"({risk.critical} critical, "

                f"{risk.high} high, "

                f"{risk.medium} medium, "

                f"{risk.low} low)."

            )

        # ==================================================
        # Forecast
        # ==================================================

        if "finish" in q or "complete" in q:

            return (

                f"Predicted completion date is "

                f"{forecast.predicted_completion}. "

                f"Estimated delay is "

                f"{forecast.estimated_delay_days} days."

            )

        # ==================================================
        # Critical Path
        # ==================================================

        if "critical" in q:

            return (

                f"There are "

                f"{len(critical.critical_path)} "

                f"critical tasks with a total "

                f"project duration of "

                f"{critical.project_duration} days."

            )

        # ==================================================
        # Delayed Tasks
        # ==================================================

        if "delay" in q:

            return (

                f"There are "

                f"{schedule.delayed_tasks} delayed tasks."

            )

        # ==================================================
        # Recommendations
        # ==================================================

        if "recommend" in q:

            if recommendation.total == 0:

                return "No recommendations available."

            top = recommendation.recommendations[0]

            return (

                f"Top recommendation: "

                f"{top.title}. "

                f"{top.description}"

            )

        return (

            "Sorry, I couldn't understand "

            "that question."

        )

    # =====================================================
    # LLM Prompt
    # =====================================================

    def build_prompt(
        self,
        question: str,
    ) -> str:

        health = self.blackboard.get(
            "health_score"
        )

        risk = self.blackboard.get(
            "risk_report"
        )

        forecast = self.blackboard.get(
            "forecast"
        )

        recommendations = self.blackboard.get(
            "recommendations"
        )

        summary = self.blackboard.get(
            "executive_summary"
        )

        prompt = f"""
You are a Senior Project Management AI Assistant.

Answer the user's question using ONLY the analytics below.

========================
PROJECT HEALTH
========================

Overall Score:
{health.overall_score}

Status:
{health.status}

========================
RISK SUMMARY
========================

Critical:
{risk.critical}

High:
{risk.high}

Medium:
{risk.medium}

Low:
{risk.low}

========================
FORECAST
========================

Completion:
{forecast.predicted_completion}

Delay Probability:
{forecast.delay_probability}

Estimated Delay:
{forecast.estimated_delay_days}

Confidence:
{forecast.confidence}

========================
TOP RECOMMENDATIONS
========================

"""

        for rec in recommendations.recommendations[:5]:

            prompt += f"""

Priority : {rec.priority}

Title : {rec.title}

Description : {rec.description}

"""

        prompt += f"""

========================
EXECUTIVE SUMMARY
========================

{summary["executive_narrative"]}

========================
QUESTION
========================

{question}

Respond like an experienced Project Director.

"""

        return prompt

    # =====================================================
    # LLM
    # =====================================================

    async def ask_llm(
        self,
        question: str,
        llm,
    ) -> str:

        prompt = self.build_prompt(
            question
        )

        answer = await llm.generate(
            prompt
        )

        return answer

    # =====================================================
    # Debug
    # =====================================================

    def print_context(self):

        print()

        print("=" * 80)

        print("QA AGENT")

        print("=" * 80)

        print()

        print(

            self.build_prompt(

                "Project Summary"

            )

        )

        print()

        print("=" * 80)