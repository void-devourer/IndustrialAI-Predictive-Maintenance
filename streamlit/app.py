import streamlit as st
import requests
import numpy as np
import pandas as pd
import os

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Industrial AI Monitoring Platform",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================

st.title("🏭 Industrial AI Monitoring Platform")
st.caption("Physics-Informed Machine Health Prediction & Industrial Decision Support")

st.markdown("---")

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("⚙ Machine Parameters")

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"]
    )

    air_temp = st.slider(
        "Air Temperature (K)",
        295.0,
        305.0,
        300.0
    )

    process_temp = st.slider(
        "Process Temperature (K)",
        305.0,
        315.0,
        310.0
    )

    rotational_speed = st.slider(
        "Rotational Speed (RPM)",
        1168,
        2886,
        1500
    )

    torque = st.slider(
        "Torque (Nm)",
        3.8,
        76.6,
        40.0
    )

    tool_wear = st.slider(
        "Tool Wear (min)",
        0,
        253,
        100
    )

    st.markdown("---")

    predict_button = st.button(
        "🚀 Predict Machine Health",
        use_container_width=True
    )

# ==========================================================
# LIVE PHYSICS CALCULATIONS
# ==========================================================

power_watts = torque * rotational_speed * (np.pi / 30)

temp_difference = process_temp - air_temp

wear_progression = tool_wear * torque

# ==========================================================
# LIVE MACHINE METRICS
# ==========================================================

st.subheader("📊 Live Physics-Based Machine Metrics")

metric1, metric2, metric3 = st.columns(3)

with metric1:

    st.metric(
        "⚡ Power Output",
        f"{power_watts:.0f} W",
        "🟢 Normal" if power_watts <= 7282 else "🔴 High"
    )

with metric2:

    st.metric(
        "🌡 Temperature Difference",
        f"{temp_difference:.1f} K",
        "🟢 Normal" if temp_difference >= 9.4 else "🟠 Cooling Risk"
    )

with metric3:

    st.metric(
        "🔧 Wear Progression",
        f"{wear_progression:.0f}",
        "🟢 Normal" if wear_progression <= 7187 else "🔴 High"
    )

st.markdown("---")

# ==========================================================
# QUICK ENGINEERING SUMMARY
# ==========================================================

st.subheader("🛠 Engineering Snapshot")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"""
**Machine Type:** {machine_type}

**Power Output:** {power_watts:.0f} W

**Temperature Difference:** {temp_difference:.1f} K
"""
    )

with summary_col2:

    st.info(
        f"""
**Tool Wear:** {tool_wear} min

**Wear Progression:** {wear_progression:.0f}

**Rotational Speed:** {rotational_speed} RPM
"""
    )

st.markdown("---")

# ==========================================================
# API CALL
# ==========================================================
API_URL = os.getenv(
    "API_URL",
    "https://industrialai-predictive-maintenance.onrender.com"
)

if predict_button:

    try:

        response = requests.post(

            f"{API_URL}/predict",

            json={

                "air_temp": air_temp,

                "process_temp": process_temp,

                "rotational_speed": rotational_speed,

                "torque": torque,

                "tool_wear": tool_wear,

                "machine_type": machine_type

            },

            timeout=5

        )

        response.raise_for_status()

        result = response.json()

        prediction = result["prediction"]
        probability = result["failure_probability"]
        risk = result["risk_level"]
        actions = result["recommended_actions"]
        request_id = result["request_id"]
        timestamp = result["timestamp"]
                # ==========================================================
        # PREDICTION RESULT
        # ==========================================================

        st.markdown("## 🤖 AI Prediction Results")

        status_col1, status_col2 = st.columns([2, 1])

        with status_col1:

            if prediction == "FAILURE":

                st.error("## 🔴 MACHINE STATUS : FAILURE PREDICTED")

            else:

                st.success("## 🟢 MACHINE STATUS : HEALTHY")

            st.metric(
                label="Failure Probability",
                value=f"{probability:.2f}%"
            )

            st.metric(
                label="Risk Level",
                value=risk
            )

        with status_col2:

            st.subheader("📋 Prediction Summary")

            st.write(f"**Prediction:** {prediction}")

            st.write(f"**Machine Type:** {machine_type}")

            st.write(f"**Timestamp:**")

            st.caption(timestamp)

        st.markdown("---")

        # ==========================================================
        # AI ENGINEERING SUMMARY
        # ==========================================================

        st.subheader("🤖 AI Engineering Summary")

        summary = []

        if power_watts > 7282:
            summary.append(
                "⚠ High mechanical power output detected. Energy consumption and mechanical loading are elevated."
            )
        else:
            summary.append(
                "✅ Power output is operating within the learned safe region."
            )

        if temp_difference < 9.4:
            summary.append(
                "⚠ Temperature difference indicates reduced cooling efficiency."
            )
        else:
            summary.append(
                "✅ Cooling performance appears normal."
            )

        if wear_progression > 7187:
            summary.append(
                "⚠ Tool wear progression suggests maintenance should be scheduled soon."
            )
        else:
            summary.append(
                "✅ Tool wear remains within acceptable operating limits."
            )

        if prediction == "FAILURE":

            summary.append(
                "🚨 The AI model predicts a high probability of machine failure. Immediate inspection is recommended."
            )

        else:

            summary.append(
                "✅ The AI model predicts normal machine operation based on the current operating conditions."
            )

        for line in summary:
            st.write(line)

        st.markdown("---")

        # ==========================================================
        # ENGINEERING RECOMMENDATIONS
        # ==========================================================

        st.subheader("🛠 Recommended Engineering Actions")

        for action in actions:

            if prediction == "FAILURE":
                st.warning(action)
            else:
                st.success(action)

        st.markdown("---")

        # ==========================================================
        # PHYSICS FEATURE SUMMARY
        # ==========================================================

        st.subheader("📈 Physics Feature Summary")

        physics1, physics2, physics3 = st.columns(3)

        with physics1:
            st.metric(
                "⚡ Power",
                f"{power_watts:.0f} W"
            )

        with physics2:
            st.metric(
                "🌡 Temp Difference",
                f"{temp_difference:.1f} K"
            )

        with physics3:
            st.metric(
                "🔧 Wear Progression",
                f"{wear_progression:.0f}"
            )

        st.markdown("---")

        # ==========================================================
        # REQUEST INFORMATION
        # ==========================================================

        with st.expander("📌 Prediction Metadata"):

            st.write(f"**Request ID:** `{request_id}`")

            st.write(f"**Timestamp:** `{timestamp}`")

            st.write("Prediction generated through FastAPI backend.")

    except requests.exceptions.ConnectionError:

        st.error("❌ FastAPI server is not running.")

    except requests.exceptions.HTTPError as e:

        st.error(f"API Error: {e}")

    except Exception as e:

        st.error(f"Unexpected Error: {e}")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "🏭 Industrial AI Monitoring Platform | FastAPI • Streamlit • Scikit-learn"
)
st.markdown("---")
st.header("📊 Prediction History")

try:
    response = requests.get(
        f"{API_URL}/history",
        timeout=5
    )

    response.raise_for_status()

    history = response.json()

    if history:

        df = pd.DataFrame(history)

        df = df.rename(
            columns={
                "timestamp": "Timestamp",
                "machine_type": "Machine",
                "prediction": "Prediction",
                "probability": "Probability (%)",
                "risk_level": "Risk"
            }
        )

        # ----------------------------
        # Filters
        # ----------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            machine_filter = st.multiselect(
                "Machine Type",
                options=sorted(df["Machine"].unique()),
                default=list(df["Machine"].unique())
            )

        with col2:
            risk_filter = st.multiselect(
                "Risk Level",
                options=sorted(df["Risk"].unique()),
                default=list(df["Risk"].unique())
            )

        with col3:
            prediction_filter = st.multiselect(
                "Prediction",
                options=sorted(df["Prediction"].unique()),
                default=list(df["Prediction"].unique())
            )

        filtered_df = df[
            df["Machine"].isin(machine_filter)
            & df["Risk"].isin(risk_filter)
            & df["Prediction"].isin(prediction_filter)
        ]

        # ----------------------------
        # History Table
        # ----------------------------

        st.subheader("Recent Predictions")

        st.dataframe(
            filtered_df,
            width="stretch",
            hide_index=True
        )

        # ----------------------------
        # CSV Export
        # ----------------------------

        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Prediction History",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv"
        )

        st.markdown("---")

        # ==========================================================
        # ANALYTICS DASHBOARD
        # ==========================================================

        st.subheader("📊 Industrial Analytics")

        # ----------------------------------------------------------
        # Prepare analytics data
        # ----------------------------------------------------------

        analytics_df = filtered_df.copy()

        total_predictions = len(analytics_df)

        failures = (
            analytics_df["Prediction"] == "FAILURE"
        ).sum()

        healthy = (
            analytics_df["Prediction"] == "HEALTHY"
        ).sum()

        critical = (
            analytics_df["Risk"] == "CRITICAL"
        ).sum()

        if total_predictions > 0:

            failure_rate = (
                failures / total_predictions
            ) * 100

            avg_probability = analytics_df[
                "Probability (%)"
            ].mean()

        else:

            failure_rate = 0
            avg_probability = 0


        # ----------------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------------

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        with kpi1:

            st.metric(
                "Total Predictions",
                total_predictions
            )

        with kpi2:

            st.metric(
                "Failures",
                failures
            )

        with kpi3:

            st.metric(
                "Healthy",
                healthy
            )

        with kpi4:

            st.metric(
                "Failure Rate",
                f"{failure_rate:.1f}%"
            )

        with kpi5:

            st.metric(
                "Critical Risk",
                critical
            )


        st.markdown("---")


        # ==========================================================
        # CHARTS
        # ==========================================================

        chart_col1, chart_col2 = st.columns(2)


        # ----------------------------------------------------------
        # Risk Distribution
        # ----------------------------------------------------------

        with chart_col1:

            st.markdown("### 🚨 Risk Distribution")

            risk_counts = (
                analytics_df["Risk"]
                .value_counts()
            )

            st.bar_chart(risk_counts)


        # ----------------------------------------------------------
        # Prediction Distribution
        # ----------------------------------------------------------

        with chart_col2:

            st.markdown("### 🤖 Machine Health")

            prediction_counts = (
                analytics_df["Prediction"]
                .value_counts()
            )

            st.bar_chart(prediction_counts)


        # ----------------------------------------------------------
        # Failure Probability
        # ----------------------------------------------------------

        st.markdown("### 📈 Failure Probability Over Time")

        if not analytics_df.empty:

            probability_chart = analytics_df[
                ["Timestamp", "Probability (%)"]
            ].copy()

            probability_chart["Timestamp"] = pd.to_datetime(
                probability_chart["Timestamp"]
            )

            probability_chart = (
                probability_chart
                .sort_values("Timestamp")
                .set_index("Timestamp")
            )

            st.line_chart(
                probability_chart
            )

        else:

            st.info(
                "No prediction data available for the selected filters."
            )


        # ----------------------------------------------------------
        # Machine Type Distribution
        # ----------------------------------------------------------

        st.markdown("### 🏭 Predictions by Machine Type")

        machine_counts = (
            analytics_df["Machine"]
            .value_counts()
        )

        st.bar_chart(machine_counts)


        # ----------------------------------------------------------
        # Analytics Summary
        # ----------------------------------------------------------

        st.markdown("---")

        st.markdown("### 🧠 System Analytics Summary")

        if total_predictions == 0:

            st.info(
                "No prediction data available for analysis."
            )

        else:

            if failure_rate >= 50:

                st.error(
                    f"⚠️ High failure rate detected: "
                    f"{failure_rate:.1f}% of predictions indicate machine failure."
                )

            elif failure_rate > 0:

                st.warning(
                    f"⚠️ {failure_rate:.1f}% of predictions indicate "
                    "potential machine failure."
                )

            else:

                st.success(
                    "✅ No machine failures detected in the current dataset."
                )

            st.write(
                f"Average predicted failure probability: "
                f"**{avg_probability:.1f}%**"
            )

            st.write(
                f"Critical-risk predictions: "
                f"**{critical}**"
            )

    else:

        st.info("No prediction history available yet.")

except requests.exceptions.ConnectionError:

    st.error("❌ FastAPI server is not running.")

except Exception as e:

    st.error(f"❌ Could not load prediction history: {e}")