from __future__ import annotations

import streamlit as st


def render():

    with st.sidebar:

        st.title("AI PM")

        st.divider()

        if st.session_state.get(
            "project_loaded",
            False,
        ):

            st.success(
                "Project Loaded"
            )

        else:

            st.warning(
                "No Project Loaded"
            )

        st.divider()

        st.caption(
            "Enterprise AI Project Intelligence"
        )