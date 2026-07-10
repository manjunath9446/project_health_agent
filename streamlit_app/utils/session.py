from __future__ import annotations

import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def initialize():

    defaults = {

        "pipeline": None,

        "project_loaded": False,

        "dashboard": None,

        "project_context": None,

        "chat_history": [],

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value