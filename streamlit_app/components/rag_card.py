import streamlit as st


def rag_card(
    health_score: float,
    rag_status: str,
    reasons: list[str] | None = None,
):
    """
    Professional RAG Status Card
    """

    rag_status = rag_status.upper()

    if rag_status == "GREEN":

        color = "#22c55e"
        bg = "#dcfce7"
        emoji = "🟢"

    elif rag_status == "AMBER":

        color = "#f59e0b"
        bg = "#fef3c7"
        emoji = "🟡"

    else:

        color = "#ef4444"
        bg = "#fee2e2"
        emoji = "🔴"

    html = f"""
    <div style="

        background:{bg};

        border-left:8px solid {color};

        border-radius:18px;

        padding:25px;

        box-shadow:0 8px 20px rgba(0,0,0,.08);

    ">

        <div style="

            font-size:14px;

            color:#6b7280;

            font-weight:700;

            letter-spacing:1px;

        ">

            PROJECT STATUS

        </div>

        <div style="

            font-size:44px;

            font-weight:800;

            color:{color};

            margin-top:10px;

        ">

            {emoji} {rag_status}

        </div>

        <div style="

            font-size:20px;

            margin-top:8px;

            color:#111827;

            font-weight:700;

        ">

            Health Score

            {health_score:.1f}%

        </div>

    """

    if reasons:

        html += """

        <hr>

        <div style="

            font-weight:700;

            margin-bottom:10px;

        ">

        Why?

        </div>

        <ul>

        """

        for reason in reasons:

            html += f"<li>{reason}</li>"

        html += "</ul>"

    html += "</div>"

    st.markdown(

        html,

        unsafe_allow_html=True,

    )