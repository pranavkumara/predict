import streamlit as st
import requests


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Predictive Maintenance",
    page_icon="⚙️",
    layout="wide"
)


# --------------------------------------------------
# API configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚙️ Predictive Maintenance System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered machine failure prediction using XGBoost'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Machine Information")

machine_type = st.sidebar.selectbox(
    "Machine Type",
    ["L", "M", "H"]
)

air_temperature = st.sidebar.number_input(
    "Air Temperature (K)",
    min_value=250.0,
    max_value=350.0,
    value=300.5,
    step=0.1
)

process_temperature = st.sidebar.number_input(
    "Process Temperature (K)",
    min_value=250.0,
    max_value=350.0,
    value=310.2,
    step=0.1
)

rotational_speed = st.sidebar.number_input(
    "Rotational Speed (RPM)",
    min_value=0.0,
    max_value=5000.0,
    value=1500.0,
    step=10.0
)

torque = st.sidebar.number_input(
    "Torque (Nm)",
    min_value=0.0,
    max_value=100.0,
    value=45.0,
    step=1.0
)

tool_wear = st.sidebar.number_input(
    "Tool Wear (min)",
    min_value=0.0,
    max_value=300.0,
    value=120.0,
    step=1.0
)


# --------------------------------------------------
# Predict button
# --------------------------------------------------

predict_button = st.sidebar.button(
    "🔍 Predict Failure",
    use_container_width=True
)


# --------------------------------------------------
# Main dashboard
# --------------------------------------------------

st.subheader("Machine Health Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Model",
        "XGBoost"
    )

with col2:

    st.metric(
        "Accuracy",
        "98.45%"
    )

with col3:

    st.metric(
        "ROC-AUC",
        "97.25%"
    )


st.divider()


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if predict_button:

    payload = {
        "machine_type": machine_type,
        "air_temperature": air_temperature,
        "process_temperature": process_temperature,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear
    }

    try:

        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            probability = result["failure_probability"]
            risk = result["risk_level"]
            recommendation = result["recommendation"]


            # --------------------------------------
            # Result header
            # --------------------------------------

            st.subheader("Prediction Result")


            col1, col2 = st.columns(2)


            with col1:

                if prediction == 1:

                    st.error(
                        "⚠️ MACHINE FAILURE RISK DETECTED"
                    )

                else:

                    st.success(
                        "✅ MACHINE OPERATING NORMALLY"
                    )


            with col2:

                st.metric(
                    "Failure Probability",
                    f"{probability * 100:.2f}%"
                )


            # --------------------------------------
            # Risk
            # --------------------------------------

            if risk == "HIGH":

                st.error(
                    f"Risk Level: **{risk}**"
                )

            elif risk == "MEDIUM":

                st.warning(
                    f"Risk Level: **{risk}**"
                )

            else:

                st.success(
                    f"Risk Level: **{risk}**"
                )


            # --------------------------------------
            # Probability bar
            # --------------------------------------

            st.write("Failure Probability")

            st.progress(
                min(probability, 1.0)
            )


            # --------------------------------------
            # Recommendation
            # --------------------------------------

            st.info(
                f"**Recommendation:** {recommendation}"
            )


            # --------------------------------------
            # Input summary
            # --------------------------------------

            st.subheader("Machine Parameters")

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric(
                "Air Temp",
                f"{air_temperature:.1f} K"
            )

            c2.metric(
                "Process Temp",
                f"{process_temperature:.1f} K"
            )

            c3.metric(
                "Speed",
                f"{rotational_speed:.0f} RPM"
            )

            c4.metric(
                "Torque",
                f"{torque:.1f} Nm"
            )

            c5.metric(
                "Tool Wear",
                f"{tool_wear:.0f} min"
            )


        else:

            st.error(
                f"API Error: {response.text}"
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI. "
            "Make sure the API server is running on port 8000."
        )


    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )


else:

    st.info(
        "Enter the machine parameters in the sidebar "
        "and click **Predict Failure**."
    )