from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.core.database import async_session
from src.services.project_pipeline_service import ProjectPipelineService

# ==========================================================
# PAGE
# ==========================================================

st.set_page_config(
    page_title="Upload Project",
    page_icon="📂",
    layout="wide",
)

st.title("📂 Upload Project Plan")

st.write(
    "Upload a Microsoft Project Excel workbook for AI analysis."
)

st.divider()

# ==========================================================
# INPUTS
# ==========================================================

project_name = st.text_input(
    "Project Name",
    placeholder="Example: SAP Implementation",
)

uploaded_file = st.file_uploader(
    "Microsoft Project Workbook",
    type=["xlsx"],
)

# ==========================================================
# BACKEND
# ==========================================================

async def analyze_project(
    project_name: str,
    file_path: str,
):

    async with async_session() as session:

        pipeline = ProjectPipelineService(session)

        dashboard = await pipeline.process_project(

            project_name=project_name,

            file_path=file_path,

        )

        return pipeline, dashboard


# ==========================================================
# BUTTON
# ==========================================================

if st.button(
    "🚀 Analyze Project",
    use_container_width=True,
):

    if not project_name:

        st.error("Enter project name.")

        st.stop()

    if uploaded_file is None:

        st.error("Upload an Excel workbook.")

        st.stop()

    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".xlsx",

    ) as temp:

        temp.write(uploaded_file.read())

        excel_path = temp.name

    progress = st.progress(0)

    status = st.empty()

    try:

        status.info("Uploading workbook...")

        progress.progress(20)

        status.info("Reading project plan...")

        progress.progress(40)

        status.info("Running AI analysis...")

        pipeline, dashboard = asyncio.run(

            analyze_project(

                project_name,

                excel_path,

            )

        )

        progress.progress(90)

        # =====================================
        # SAVE RESULTS
        # =====================================

        st.session_state.project_loaded = True

        st.session_state.project_name = project_name

        st.session_state.pipeline = pipeline

        st.session_state.dashboard = dashboard

        progress.progress(100)

        status.success("Analysis Complete")

        st.success(
            "Project analyzed successfully."
        )

    except Exception as e:

        st.exception(e)

    finally:

        try:

            Path(excel_path).unlink(
                missing_ok=True,
            )
        except Exception:
            pass

# ==========================================================
# AFTER ANALYSIS
# ==========================================================

if st.session_state.project_loaded:

    st.divider()

    st.success(
        "Project successfully loaded."
    )

    st.write(
        f"**Project:** {st.session_state.project_name}"
    )

    if st.button(
        "➡ View RAG Status",
        use_container_width=True,
        type="primary",
    ):

        st.switch_page(
            "pages/2_🚦_RAG_Status.py"
        )

else:

    st.info(
        "Upload a project and click Analyze Project."
    )