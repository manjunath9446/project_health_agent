import streamlit as st


def recommendation_card(

    title,

    priority,

    category,

    description,

    impact,

):

    colors = {

        "HIGH": "#ef4444",

        "MEDIUM": "#f59e0b",

        "LOW": "#22c55e",

    }

    color = colors.get(

        str(priority).upper(),

        "#2563eb",

    )

    st.markdown(

        f"""
<div style="

background:white;

padding:20px;

border-radius:15px;

border-left:7px solid {color};

margin-bottom:16px;

box-shadow:0 5px 15px rgba(0,0,0,.08);

">

<h3>

{title}

</h3>

<b>Priority</b>

{priority}

<br>

<b>Category</b>

{category}

<br><br>

{description}

<br><br>

<b>Expected Impact</b>

<ul>

<li>

{impact}

</li>

</ul>

</div>
""",

        unsafe_allow_html=True,

    )