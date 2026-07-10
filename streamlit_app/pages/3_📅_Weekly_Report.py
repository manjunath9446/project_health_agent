from __future__ import annotations

from datetime import datetime
import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Weekly Report",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Weekly Project Status Report")

st.write(
    "AI-generated weekly project health report."
)

st.divider()

# ==========================================================
# CHECK PROJECT
# ==========================================================

if not st.session_state.get("project_loaded", False):

    st.warning(
        "Please upload and analyze a project first."
    )

    st.stop()

dashboard = st.session_state.dashboard

health = dashboard["health"]
forecast = dashboard["forecast"]
risk = dashboard["risk_report"]
summary = dashboard["executive_summary"]
recommendations = dashboard["recommendations"]

# ==========================================================
# RAG
# ==========================================================

score = health.overall_score

if score >= 80:

    rag = "🟢 GREEN"

elif score >= 60:

    rag = "🟡 AMBER"

else:

    rag = "🔴 RED"

# ==========================================================
# HEADER
# ==========================================================

st.subheader("Project Information")

st.write(f"**Project Name:** {st.session_state.project_name}")

st.write(f"**Report Date:** {datetime.now():%d %B %Y}")

st.write(f"**Overall RAG Status:** {rag}")

st.divider()

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("Executive Summary")

if isinstance(summary, dict):

    narrative = summary.get(
        "executive_narrative",
        summary,
    )

else:

    narrative = summary

if isinstance(narrative, list):

    for para in narrative:

        st.write(para)

else:

    st.write(narrative)

st.divider()

# ==========================================================
# PROJECT HEALTH
# ==========================================================

st.subheader("Project Health")

st.write(f"**Overall Health Score:** {health.overall_score:.1f}%")

st.write(f"**Forecast Delay:** {forecast.estimated_delay_days} Days")

st.write(f"**Delay Probability:** {forecast.delay_probability:.0f}%")

st.write(f"**Critical Risks:** {risk.critical}")

st.divider()

# ==========================================================
# TOP RISKS
# ==========================================================

st.subheader("Top Risks")

if len(risk.risks) == 0:

    st.success("No significant risks identified.")

else:

    for index, item in enumerate(risk.risks[:5], start=1):

        st.markdown(f"### {index}. {item.task_name}")

        st.write(f"**Risk Type:** {item.risk_type}")

        st.write(f"**Severity:** {item.level}")

        st.write(item.message)

        st.write(f"**Recommendation:** {item.recommendation}")

        st.write("---")

# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.subheader("Recommended Actions")

if recommendations.recommendations:

    for index, rec in enumerate(
        recommendations.recommendations,
        start=1,
    ):

        st.markdown(f"### {index}. {rec.title}")

        st.write(rec.description)

        st.write(f"Priority: {rec.priority}")

        st.write(f"Category: {rec.category}")

        st.write("---")

else:

    st.info("No recommendations available.")

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

report = f"""
WEEKLY PROJECT STATUS REPORT

Project:
{st.session_state.project_name}

Date:
{datetime.now():%d %B %Y}

Overall RAG:
{rag}

Health Score:
{health.overall_score:.1f}%

Forecast Delay:
{forecast.estimated_delay_days} Days

Delay Probability:
{forecast.delay_probability:.0f}%

Critical Risks:
{risk.critical}
"""

st.download_button(

    label="📥 Download Weekly Report",

    data=report,

    file_name="Weekly_Project_Report.txt",

    mime="text/plain",

    use_container_width=True,

)

st.divider()

if st.button(

    "Next → Monthly Executive Presentation",

    use_container_width=True,

):

    st.switch_page(

        "pages/4_📊_Monthly_Presentation.py"

    )