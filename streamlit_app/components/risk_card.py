import streamlit as st


def risk_card(

    task,

    risk_type,

    severity,

    reason,

    recommendation,

):

    colors = {

        "CRITICAL": "#dc2626",

        "HIGH": "#ea580c",

        "MEDIUM": "#ca8a04",

        "LOW": "#16a34a",

    }

    color = colors.get(

        str(severity).upper(),

        "#2563eb",

    )

    st.markdown(

        f"""
<div style="

background:white;

padding:20px;

border-left:8px solid {color};

border-radius:15px;

margin-bottom:14px;

box-shadow:0 5px 15px rgba(0,0,0,.08);

">

<h3>

{task}

</h3>

<b>Risk Type</b>

{risk_type}

<br>

<b>Severity</b>

{severity}

<br><br>

{reason}

<br><br>

<b>Recommendation</b>

<ul>

<li>

{recommendation}

</li>

</ul>

</div>
""",

        unsafe_allow_html=True,

    )