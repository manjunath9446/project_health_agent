from __future__ import annotations

from loguru import logger

from src.core.blackboard import Blackboard


class ExecutiveSummaryAgent:
    """
    Generates an executive-level summary of the project.

    Reads analytics outputs from the Blackboard and produces
    a concise business summary.

    Input

        • Health Score
        • Risk Report
        • Forecast
        • Recommendations
        • Critical Path

    Output

        executive_summary
    """

    def __init__(
        self,
        blackboard: Blackboard,
    ):

        self.blackboard = blackboard

    # =====================================================

    def run(self):

        logger.info(
            "ExecutiveSummaryAgent started."
        )

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

        critical = self.blackboard.get(
            "critical_path"
        )

        summary = self._build_summary(

            health,

            risk,

            forecast,

            recommendations,

            critical,

        )

        self.blackboard.put(

            key="executive_summary",

            value=summary,

            producer="ExecutiveSummaryAgent",

        )

        logger.success(
            "Executive summary generated."
        )

    # =====================================================
    # Build Summary
    # =====================================================

    def _build_summary(

        self,

        health,

        risk,

        forecast,

        recommendations,

        critical,

    ) -> dict:

        summary = {}

        # -------------------------------------------------
        # Overall Health
        # -------------------------------------------------

        summary["overall_health"] = {

            "score": health.overall_score,

            "status": health.status,

        }

        # -------------------------------------------------
        # Risk Summary
        # -------------------------------------------------

        summary["risks"] = {

            "total": risk.total,

            "critical": risk.critical,

            "high": risk.high,

            "medium": risk.medium,

            "low": risk.low,

        }

        # -------------------------------------------------
        # Forecast
        # -------------------------------------------------

        summary["forecast"] = {

            "predicted_completion":
                forecast.predicted_completion,

            "delay_probability":
                forecast.delay_probability,

            "estimated_delay_days":
                forecast.estimated_delay_days,

            "confidence":
                forecast.confidence,

        }

        # -------------------------------------------------
        # Critical Path
        # -------------------------------------------------

        summary["critical_path"] = {

            "project_duration":
                critical.project_duration,

            "critical_tasks":
                len(critical.critical_path),

        }

        # -------------------------------------------------
        # Top Recommendations
        # -------------------------------------------------

        summary["recommendations"] = [

            {

                "priority": str(rec.priority),

                "title": rec.title,

                "category": rec.category,

            }

            for rec in recommendations.recommendations[:5]

        ]

        # =====================================================
        # Executive Narrative
        # =====================================================

        narrative = []

        # -------------------------------------------------
        # Overall Health
        # -------------------------------------------------

        if health.overall_score >= 90:

            narrative.append(
                "The project is in excellent health with strong execution across schedule, risks, and dependencies."
            )

        elif health.overall_score >= 75:

            narrative.append(
                "The project is progressing well with only minor issues requiring attention."
            )

        elif health.overall_score >= 60:

            narrative.append(
                "The project is moderately healthy but requires management focus in several areas."
            )

        elif health.overall_score >= 40:

            narrative.append(
                "The project is at risk and corrective actions should be initiated immediately."
            )

        else:

            narrative.append(
                "The project is in a critical state and requires executive intervention."
            )

        # -------------------------------------------------
        # Risks
        # -------------------------------------------------

        if risk.critical > 0:

            narrative.append(

                f"{risk.critical} critical risks require immediate attention."

            )

        elif risk.high > 0:

            narrative.append(

                f"{risk.high} high-severity risks have been identified."

            )

        else:

            narrative.append(

                "No major project risks have been detected."

            )

        # -------------------------------------------------
        # Forecast
        # -------------------------------------------------

        if forecast.delay_probability >= 70:

            narrative.append(

                f"There is a high probability ({forecast.delay_probability:.1f}%) of project delay."

            )

        elif forecast.delay_probability >= 40:

            narrative.append(

                f"There is a moderate probability ({forecast.delay_probability:.1f}%) of schedule slippage."

            )

        else:

            narrative.append(

                "Current forecast indicates a low likelihood of schedule delay."

            )

        # -------------------------------------------------
        # Critical Path
        # -------------------------------------------------

        narrative.append(

            f"The project contains {len(critical.critical_path)} critical path tasks with an estimated duration of {critical.project_duration} days."

        )

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        if recommendations.total > 0:

            top = recommendations.recommendations[0]

            narrative.append(

                f"Highest priority recommendation: {top.title}."

            )

        summary["executive_narrative"] = narrative

        return summary
        # =====================================================
    # Print Summary
    # =====================================================

    @staticmethod
    def print_summary(
        summary: dict,
    ) -> None:

        print()

        print("=" * 90)

        print("EXECUTIVE SUMMARY")

        print("=" * 90)

        print()

        health = summary["overall_health"]

        print(
            f"Overall Health : {health['score']:.2f}% ({health['status']})"
        )

        print()

        risks = summary["risks"]

        print(
            "Risks"
        )

        print(
            f"  Total     : {risks['total']}"
        )

        print(
            f"  Critical  : {risks['critical']}"
        )

        print(
            f"  High      : {risks['high']}"
        )

        print(
            f"  Medium    : {risks['medium']}"
        )

        print(
            f"  Low       : {risks['low']}"
        )

        print()

        forecast = summary["forecast"]

        print(
            "Forecast"
        )

        print(
            f"  Completion Date : {forecast['predicted_completion']}"
        )

        print(
            f"  Delay Probability : {forecast['delay_probability']:.2f}%"
        )

        print(
            f"  Estimated Delay : {forecast['estimated_delay_days']} days"
        )

        print(
            f"  Confidence : {forecast['confidence']:.2f}%"
        )

        print()

        cp = summary["critical_path"]

        print(
            "Critical Path"
        )

        print(
            f"  Duration : {cp['project_duration']} days"
        )

        print(
            f"  Critical Tasks : {cp['critical_tasks']}"
        )

        print()

        print("-" * 90)

        print("Executive Narrative")

        print("-" * 90)

        for line in summary["executive_narrative"]:

            print(f"• {line}")

        print()

        print("-" * 90)

        print("Top Recommendations")

        print("-" * 90)

        if summary["recommendations"]:

            for recommendation in summary["recommendations"]:

                print(

                    f"[{recommendation['priority']}] "
                    f"{recommendation['title']} "
                    f"({recommendation['category']})"

                )

        else:

            print("No recommendations.")

        print()

        print("=" * 90)

    # =====================================================
    # Blackboard Helper
    # =====================================================

    def get_summary(self) -> dict:

        return self.blackboard.get(
            "executive_summary"
        )