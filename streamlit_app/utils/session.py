from __future__ import annotations

import streamlit as st


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