import streamlit as st


def no_project():

    st.markdown(

        """
<div style="

background:white;

padding:60px;

text-align:center;

border-radius:18px;

border:2px dashed #cbd5e1;

">

<h1>

📂

</h1>

<h2>

No Project Loaded

</h2>

<p>

Upload a Microsoft Project workbook to begin.

</p>

</div>
""",

        unsafe_allow_html=True,

    )