from __future__ import annotations

import asyncio
import tempfile
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.core.database import async_session, init_db
from src.services.project_pipeline_service import ProjectPipelineService

# ==========================================================
# PAGE CONFIG
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
# SESSION STATE
# ==========================================================

if "project_loaded" not in st.session_state:
    st.session_state.project_loaded = False

if "dashboard" not in st.session_state:
    st.session_state.dashboard = None

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if "project_name" not in st.session_state:
    st.session_state.project_name = ""

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
    # Ensure database exists
    await init_db()

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