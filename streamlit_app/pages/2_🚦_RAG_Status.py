from __future__ import annotations

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# PAGE
# ==========================================================

st.set_page_config(

    page_title="AI Project Assessment",

    page_icon="🚦",

    layout="wide",

)

st.title("🚦 AI Project Assessment")

st.write(
    """
The AI agent has analyzed the uploaded project plan and
determined the overall project health.
"""
)

st.divider()

# ==========================================================
# CHECK
# ==========================================================

if not st.session_state.get("project_loaded"):

    st.warning("Please upload a project first.")

    st.stop()

dashboard = st.session_state.dashboard

health = dashboard["health"]

forecast = dashboard["forecast"]

risk = dashboard["risk_report"]

summary = dashboard["executive_summary"]

recommendations = dashboard["recommendations"]

# ==========================================================
# DETERMINE RAG
# ==========================================================

score = health.overall_score

if score >= 80:

    rag = "🟢 GREEN"

elif score >= 60:

    rag = "🟡 AMBER"

else:

    rag = "🔴 RED"

# ==========================================================
# RAG
# ==========================================================

st.subheader("Overall Project Status")

st.success(rag)

st.metric(

    "Project Health Score",

    f"{score:.1f}%"

)

st.divider()

# ==========================================================
# WHY
# ==========================================================

st.subheader("Why did the AI choose this status?")

reasons = []

if forecast.delay_probability >= 70:

    reasons.append(

        f"Delay probability is {forecast.delay_probability:.0f}%."

    )

if forecast.estimated_delay_days > 0:

    reasons.append(

        f"Forecast predicts a delay of {forecast.estimated_delay_days} days."

    )

if risk.critical > 0:

    reasons.append(

        f"{risk.critical} critical risks detected."

    )

if risk.high > 0:

    reasons.append(

        f"{risk.high} high-priority risks detected."

    )

if len(reasons) == 0:

    st.success(

        "No major project health concerns detected."

    )

else:

    for reason in reasons:

        st.write("•", reason)

st.divider()

# ==========================================================
# PLAIN ENGLISH
# ==========================================================

st.subheader("Plain-English Explanation")

if isinstance(summary, dict):

    explanation = summary.get(

        "executive_narrative",

        summary,

    )

else:

    explanation = summary

if isinstance(explanation, list):

    for paragraph in explanation:

        st.write(paragraph)

else:

    st.write(explanation)

st.divider()

# ==========================================================
# DATA QUALITY
# ==========================================================

st.subheader("Data Quality Assessment")

issues = []

# Optional fields – only display if available
if "data_quality" in dashboard:

    quality = dashboard["data_quality"]

    issues = getattr(quality, "issues", [])

if len(issues) == 0:

    st.success(

        """
The project data was successfully processed.

No major data quality issues affected the AI analysis.
"""
    )

else:

    st.warning(

        "The AI detected incomplete or messy project data."

    )

    for issue in issues:

        st.write("•", issue)

st.divider()

# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.subheader("Recommended Actions")

if recommendations.recommendations:

    for index, rec in enumerate(

        recommendations.recommendations,

        start=1,

    ):

        st.write(f"### {index}. {rec.title}")

        st.write(rec.description)

        st.write(
            f"Priority : {rec.priority}"
        )

        st.write("---")

else:

    st.info(

        "No recommendations generated."

    )

st.divider()

if st.button(

    "Generate Weekly Report",

    use_container_width=True,

):

    st.switch_page(

        "pages/3_📅_Weekly_Report.py"

    )