import streamlit as st


def kpi_card(
    title: str,
    value: str | int | float,
    icon: str = "📊",
    subtitle: str = "",
    color: str = "#2563eb",
):
    """
    Modern KPI Card
    """

    html = f"""
    <div style="
        background:white;
        border-radius:18px;
        padding:20px;
        border-top:5px solid {color};
        box-shadow:0 8px 18px rgba(0,0,0,.08);
        min-height:150px;
    ">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <div style="
                font-size:15px;
                font-weight:600;
                color:#6b7280;
            ">
                {title}
            </div>

            <div style="
                font-size:34px;
            ">
                {icon}
            </div>

        </div>

        <div style="
            font-size:38px;
            font-weight:800;
            color:#111827;
            margin-top:18px;
        ">
            {value}
        </div>

        <div style="
            color:#6b7280;
            margin-top:8px;
            font-size:14px;
        ">
            {subtitle}
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Dashboard KPI Row
# ------------------------------------------------------------

def dashboard_metrics(
    health,
    delay,
    probability,
    risks,
):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            title="Health Score",
            value=f"{health:.1f}%",
            icon="💚" if health >= 80 else "❤️",
            subtitle="Overall Project Health",
            color="#22c55e" if health >= 80 else "#ef4444",
        )

    with c2:
        kpi_card(
            title="Forecast Delay",
            value=f"{delay} Days",
            icon="📅",
            subtitle="Predicted Delay",
            color="#f59e0b",
        )

    with c3:
        kpi_card(
            title="Delay Probability",
            value=f"{probability:.0f}%",
            icon="⚠️",
            subtitle="ML Prediction",
            color="#ef4444",
        )

    with c4:
        kpi_card(
            title="Critical Risks",
            value=risks,
            icon="🚨",
            subtitle="Requires Attention",
            color="#dc2626",
        )