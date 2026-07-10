from __future__ import annotations

import asyncio
import streamlit as st

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Project Insights")

st.caption(
    "Ask AI anything about the uploaded project."
)

# =====================================================
# CHECK PROJECT
# =====================================================

if not st.session_state.get("project_loaded", False):

    st.warning(
        "Please upload a project first."
    )

    st.stop()

pipeline = st.session_state.pipeline

# =====================================================
# CHAT HISTORY
# =====================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

st.subheader("Suggested Questions")

questions = [

    "Why is the project RED?",

    "Explain the RAG status.",

    "What are the biggest project risks?",

    "Which milestones are at risk?",

    "Why is delay predicted?",

    "How can the project recover?",

    "Summarize the project for a VP.",

    "What should I do this week?",

]

cols = st.columns(2)

for index, question in enumerate(questions):

    with cols[index % 2]:

        if st.button(

            question,

            use_container_width=True,

        ):

            st.session_state["prompt"] = question

# =====================================================
# ASK LLM
# =====================================================

async def ask_ai(question: str):

    return await pipeline.ask(question)

# =====================================================
# SHOW CHAT
# =====================================================

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================================
# USER INPUT
# =====================================================

prompt = st.chat_input(
    "Ask about your project..."
)

if "prompt" in st.session_state:

    prompt = st.session_state["prompt"]

    del st.session_state["prompt"]

# =====================================================
# AI RESPONSE
# =====================================================

if prompt:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing project..."):

            try:

                answer = asyncio.run(
                    ask_ai(prompt)
                )

            except Exception as exc:

                answer = str(exc)

            st.markdown(answer)

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

# =====================================================
# PROJECT SNAPSHOT
# =====================================================

st.divider()

dashboard = st.session_state.dashboard

health = dashboard["health"]

forecast = dashboard["forecast"]

risk = dashboard["risk_report"]

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(

        "Health",

        f"{health.overall_score:.1f}%"

    )

with c2:

    st.metric(

        "Forecast Delay",

        f"{forecast.estimated_delay_days} Days"

    )

with c3:

    st.metric(

        "Critical Risks",

        risk.critical

    )

# =====================================================
# ACTIONS
# =====================================================

st.divider()

left, right = st.columns(2)

with left:

    if st.button(

        "🗑 Clear Conversation",

        use_container_width=True,

    ):

        st.session_state.chat_history = []

        st.rerun()

with right:

    chat = ""

    for item in st.session_state.chat_history:

        chat += f"{item['role'].upper()}\n"

        chat += item["content"]

        chat += "\n\n"

    st.download_button(

        "📥 Download Conversation",

        data=chat,

        file_name="AI_Project_Insights.txt",

        mime="text/plain",

        use_container_width=True,

    )