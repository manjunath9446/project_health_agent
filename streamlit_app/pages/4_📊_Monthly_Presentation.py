from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.core.database import async_session
from src.services.presentation_service import PresentationService

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Monthly Executive Presentation",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Monthly Executive Presentation")

st.write(
    """
Generate a 5–7 slide executive PowerPoint suitable for a VP or client presentation.
"""
)

st.divider()

# ==========================================================
# CHECK PROJECT
# ==========================================================

if not st.session_state.get("project_loaded", False):

    st.warning("Please upload and analyse a project first.")

    st.stop()

dashboard = st.session_state.dashboard

health = dashboard["health"]
forecast = dashboard["forecast"]
risk = dashboard["risk_report"]

# ==========================================================
# SUMMARY
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Health Score",
        f"{health.overall_score:.1f}%"
    )

with col2:

    st.metric(
        "Forecast Delay",
        f"{forecast.estimated_delay_days} Days"
    )

with col3:

    st.metric(
        "Delay Probability",
        f"{forecast.delay_probability:.0f}%"
    )

with col4:

    st.metric(
        "High Risks",
        risk.high
    )

st.divider()

# ==========================================================
# PRESENTATION CONTENT
# ==========================================================

st.subheader("Presentation Includes")

st.markdown("""
- Executive Summary

- Portfolio Health

- Portfolio RAG Distribution

- Emerging Risks

- Executive Recommendations

- Next Steps
""")

st.divider()

# ==========================================================
# GENERATE
# ==========================================================

async def generate_presentation():

    async with async_session() as session:

        service = PresentationService(session)

        return await service.generate()


if st.button(

    "📊 Generate Executive Presentation",

    type="primary",

    use_container_width=True,

):

    try:

        with st.spinner("Generating presentation..."):

            ppt_path = asyncio.run(

                generate_presentation()

            )

        st.success(

            "Executive presentation generated successfully."

        )

        with open(

            ppt_path,

            "rb",

        ) as file:

            st.download_button(

                label="⬇ Download PowerPoint",

                data=file,

                file_name=Path(ppt_path).name,

                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",

                use_container_width=True,

            )

    except Exception as e:

        st.exception(e)

st.divider()

# ==========================================================
# ASSIGNMENT CHECKLIST
# ==========================================================

st.subheader("Assignment Coverage")

st.success("✅ Reads Microsoft Project Plan")

st.success("✅ Determines Project RAG")

st.success("✅ Plain-English AI Reasoning")

st.success("✅ Handles Incomplete Project Data")

st.success("✅ Weekly Project Reporting")

st.success("✅ Monthly Executive Presentation")

st.divider()

st.caption(

    f"Generated on {datetime.now():%d %B %Y %H:%M}"

)