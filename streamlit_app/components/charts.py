import plotly.graph_objects as go
import streamlit as st


# ==========================================================
# Gauge Chart
# ==========================================================

def gauge_chart(
    title: str,
    value: float,
    color="#2563eb",
):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=value,

            number={

                "suffix": "%",

                "font": {

                    "size": 40,

                },

            },

            title={

                "text": title,

                "font": {

                    "size": 18,

                },

            },

            gauge={

                "axis": {

                    "range": [0, 100],

                },

                "bar": {

                    "color": color,

                },

                "steps": [

                    {

                        "range": [0, 40],

                        "color": "#fee2e2",

                    },

                    {

                        "range": [40, 70],

                        "color": "#fef3c7",

                    },

                    {

                        "range": [70, 100],

                        "color": "#dcfce7",

                    },

                ],

            },

        )

    )

    fig.update_layout(

        height=260,

        margin=dict(

            l=20,

            r=20,

            t=50,

            b=20,

        ),

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )


# ==========================================================
# Donut Risk Chart
# ==========================================================

def risk_donut(

    critical,

    high,

    medium,

    low,

):

    fig = go.Figure(

        data=[

            go.Pie(

                labels=[

                    "Critical",

                    "High",

                    "Medium",

                    "Low",

                ],

                values=[

                    critical,

                    high,

                    medium,

                    low,

                ],

                hole=.62,

            )

        ]

    )

    fig.update_layout(

        title="Risk Distribution",

        height=420,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )


# ==========================================================
# Horizontal Bar
# ==========================================================

def health_bar(

    schedule,

    execution,

    dependency,

    risk,

    critical_path,

):

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=[

                schedule,

                execution,

                dependency,

                risk,

                critical_path,

            ],

            y=[

                "Schedule",

                "Execution",

                "Dependency",

                "Risk",

                "Critical Path",

            ],

            orientation="h",

        )

    )

    fig.update_layout(

        title="Health Components",

        height=420,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )


# ==========================================================
# Delay Chart
# ==========================================================

def delay_probability(

    probability,

):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=probability,

            number={

                "suffix": "%",

            },

            title={

                "text": "Delay Probability",

            },

            gauge={

                "axis": {

                    "range": [0,100],

                },

                "bar": {

                    "color":"crimson",

                },

            },

        )

    )

    fig.update_layout(

        height=260,

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )