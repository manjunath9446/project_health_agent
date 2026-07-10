import streamlit as st


def page_header(

    title: str,

    subtitle: str = "",

    icon: str = "📊",

):

    st.markdown(

        f"""
<div style="

background:white;

padding:28px;

border-radius:18px;

border:1px solid #e5e7eb;

box-shadow:0 8px 18px rgba(0,0,0,.08);

margin-bottom:20px;

">

<div style="

font-size:42px;

font-weight:800;

">

{icon} {title}

</div>

<div style="

margin-top:10px;

font-size:17px;

color:#6b7280;

">

{subtitle}

</div>

</div>
""",

        unsafe_allow_html=True,

    )