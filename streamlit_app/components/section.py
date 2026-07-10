import streamlit as st


def section(title: str):

    st.markdown(

        f"""
<div style="

margin-top:25px;

margin-bottom:15px;

">

<h2>

{title}

</h2>

</div>
""",

        unsafe_allow_html=True,

    )