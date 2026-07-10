import streamlit as st


def status_badge(status: str):

    status = status.upper()

    if status == "GREEN":

        color = "#16a34a"

        bg = "#dcfce7"

    elif status == "AMBER":

        color = "#ca8a04"

        bg = "#fef3c7"

    else:

        color = "#dc2626"

        bg = "#fee2e2"

    st.markdown(

        f"""
<div style="

display:inline-block;

padding:10px 22px;

background:{bg};

color:{color};

border-radius:30px;

font-size:18px;

font-weight:700;

">

{status}

</div>
""",

        unsafe_allow_html=True,

    )