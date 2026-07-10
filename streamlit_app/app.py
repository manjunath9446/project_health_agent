from __future__ import annotations

import streamlit as st
import sys
from pathlib import Path
st.write("GROQ Exists:", "GROQ_API_KEY" in os.environ)
st.write("Value:", os.getenv("GROQ_API_KEY"))

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Project Health Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULTS = {

    "project_loaded": False,

    "project_name": "",

    "dashboard": None,

    "pipeline": None,

}

for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🚦 AI Project Health")

    st.caption("Assignment Submission")

    st.divider()

    st.page_link(

        "pages/1_📂_Upload_Project.py",

        label="Upload Project",

        icon="📂",

    )

    st.page_link(

        "pages/2_🚦_RAG_Status.py",

        label="RAG Status",

        icon="🚦",

    )

    st.page_link(

        "pages/3_📅_Weekly_Report.py",

        label="Weekly Report",

        icon="📅",

    )

    st.page_link(

        "pages/4_📊_Monthly_Presentation.py",

        label="Monthly Presentation",

        icon="📊",

    )

    st.divider()

    if st.session_state.project_loaded:

        st.success("Project Loaded")

        st.write(st.session_state.project_name)

    else:

        st.warning("No Project Loaded")

# ==========================================================
# MAIN
# ==========================================================

st.title("AI Project Health Intelligence")

st.write(
    """
This application analyzes Microsoft Project plans using AI.

### Features

- Read Microsoft Project Excel files
- Determine Project RAG Status
- Explain RAG Status in plain English
- Handle incomplete project data
- Generate Weekly Project Reports
- Generate Monthly Executive Presentation
"""
)

st.divider()

st.subheader("Assignment Workflow")

st.markdown(
"""
### Phase 1

📂 Upload Microsoft Project Excel

↓

AI analyzes the project

↓

Determines RAG Status

↓

Explains the reasoning

---

### Phase 2

Generate Weekly Project Status Report

---

### Phase 3

Generate Monthly Executive Presentation
"""
)

st.divider()

if st.session_state.project_loaded:

    st.success(

        f"Current Project : {st.session_state.project_name}"

    )

    st.info(

        "Use the left sidebar to view the RAG Status, Weekly Report, or Executive Presentation."

    )

else:

    st.warning(

        "Start by uploading a Microsoft Project workbook."

    )

    st.page_link(

        "pages/1_📂_Upload_Project.py",

        label="Go to Upload Project",

        icon="📂",

    )

st.divider()

st.caption(
    "AI Project Health Intelligence • 2026 Assignment"
)