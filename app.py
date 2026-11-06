import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime
from sklearn.ensemble import IsolationForest

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="ASTROCARE",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ASTROCARE")
st.subheader("Astronaut Health Monitoring System")

st.caption(
    "A demonstration platform for monitoring astronaut health "
    "during space missions."
)

# ---------------------------------
# SESSION STATE
# ---------------------------------

# ---------------------------------
# INDIVIDUAL ASTRONAUT DATA STORAGE
# ---------------------------------

if "astronaut_health_data" not in st.session_state:
    st.session_state.astronaut_health_data = {}

if "astronaut_current_readings" not in st.session_state:
    st.session_state.astronaut_current_readings = {}

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "current_reading" not in st.session_state:

    st.session_state.current_reading = {}

if "live_data" not in st.session_state:

    st.session_state.live_data = []

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.title("🛰️ Mission Control")

# ---------------------------------
# MULTIPLE ASTRONAUT PROFILES
# ---------------------------------

astronaut_profiles = {
    "AST-001": {
        "name": "Astronaut One",
        "mission": "Mission Alpha",
        "role": "Commander"
    },

    "AST-002": {
        "name": "Astronaut Two",
        "mission": "Mission Alpha",
        "role": "Flight Engineer"
    },

    "AST-003": {
        "name": "Astronaut Three",
        "mission": "Mission Beta",
        "role": "Mission Specialist"
    }
}

astronaut_id = st.sidebar.selectbox(
    "Select Astronaut",
    list(astronaut_profiles.keys())
)

selected_profile = astronaut_profiles[astronaut_id]

astronaut_name = selected_profile["name"]
mission_name = selected_profile["mission"]
crew_role = selected_profile["role"]

st.sidebar.markdown("---")

st.sidebar.info(
    "ASTROCARE is currently using simulated health readings. "
    "It is not connected to real astronaut sensors."
)


# ---------------------------------
# SIMULATE HEALTH READINGS
# ---------------------------------

def generate_reading():

    # Create storage for the selected astronaut
    if astronaut_id not in st.session_state.astronaut_health_data:
        st.session_state.astronaut_health_data[astronaut_id] = []

    if astronaut_id not in st.session_state.astronaut_current_readings:
        st.session_state.astronaut_current_readings[astronaut_id] = {
            "Heart Rate": 72,
            "SpO2": 98,
            "Temperature": 36.8,
            "Stress": 25,
            "Activity": 30,
            "Sleep": 7.5
        }

    previous = st.session_state.astronaut_current_readings[astronaut_id]

    heart_rate = int(np.clip(
        previous["Heart Rate"] + np.random.randint(-4, 5),
        55, 125
    ))

    spo2 = int(np.clip(
        previous["SpO2"] + np.random.randint(-1, 2),
        90, 100
    ))

    temperature = round(np.clip(
        previous["Temperature"] + np.random.uniform(-0.1, 0.1),
        36.0, 38.0
    ), 1)

    stress = int(np.clip(
        previous["Stress"] + np.random.randint(-5, 6),
        0, 100
    ))

    activity = int(np.clip(
        previous["Activity"] + np.random.randint(-5, 6),
        0, 100
    ))

    sleep = previous["Sleep"]

    reading = {
        "Time": datetime.now(),
        "Heart Rate": heart_rate,
        "SpO2": spo2,
        "Temperature": temperature,
        "Stress": stress,
        "Activity": activity,
        "Sleep": sleep
    }

    # Save selected astronaut's current reading
    st.session_state.astronaut_current_readings[astronaut_id] = reading

    # Save selected astronaut's history
    st.session_state.astronaut_health_data[astronaut_id].append(reading)

    # Keep only the latest 100 readings
    st.session_state.astronaut_health_data[astronaut_id] = (
        st.session_state.astronaut_health_data[astronaut_id][-100:]
    )

    # Update dashboard variables
    st.session_state.current_reading = reading
    st.session_state.live_data = (
        st.session_state.astronaut_health_data[astronaut_id]
    )
# ---------------------------------
# ASTRONAUT PROFILE
# ---------------------------------

st.markdown("---")

st.header("👨‍🚀 Astronaut Profile")

col1, col2 = st.columns(2)

with col1:
    st.info(f"👤 **Astronaut Name:** {astronaut_name}")
    st.info(f"🆔 **Astronaut ID:** {astronaut_id}")

with col2:
    st.info(f"🚀 **Mission Name:** {mission_name}")
    st.info(f"🎖️ **Crew Role:** {crew_role}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Monitoring", use_container_width=True):
        st.session_state.monitoring = True
        generate_reading()

with col2:
    if st.button("⏹ Stop Monitoring", use_container_width=True):
        st.session_state.monitoring = False


if st.session_state.monitoring:
    st.success("Monitoring is ACTIVE")
else:
    st.warning("Monitoring is STOPPED")


# ---------------------------------
# LIVE DASHBOARD
# ---------------------------------

@st.fragment(run_every="3s")
def live_dashboard():

    if st.session_state.monitoring:

        generate_reading()

    reading = st.session_state.current_reading

        # ---------------------------------
    # AI ANOMALY DETECTION
    # ---------------------------------

    st.markdown("### 🤖 AI-Based Anomaly Detection")

    if len(st.session_state.live_data) >= 12:

        df_ai = pd.DataFrame(st.session_state.live_data)

        features = [
            "Heart Rate",
            "SpO2",
            "Temperature",
            "Stress",
            "Activity"
        ]

        # Use earlier readings to train the model
        training_data = df_ai[features].iloc[:-1]

        # Analyse the latest reading
        latest_data = df_ai[features].iloc[[-1]]

        model = IsolationForest(
            n_estimators=100,
            contamination=0.10,
            random_state=42
        )

        model.fit(training_data)

        prediction = model.predict(latest_data)

        if prediction[0] == -1:

            st.error(
                "⚠️ AI DETECTED AN UNUSUAL HEALTH PATTERN!"
            )

            st.write(
                "The machine-learning model identified "
                "the latest reading as unusual compared "
                "with previous readings."
            )

        else:

            st.success(
                "✅ No unusual pattern detected in the latest reading."
            )

        st.caption(
            "Algorithm: Isolation Forest | "
            "Training data: Previously recorded simulated readings."
        )

    else:

        st.info(
            "Collecting health readings. "
            "At least 12 readings are required before AI analysis."
        )

        st.markdown("---")

    st.markdown("### Current Health Readings")

    if reading:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "❤️ Heart Rate",
            f"{reading.get('Heart Rate', 'N/A')} BPM"
        )

        c2.metric(
            "🫁 Blood Oxygen",
            f"{reading.get('SpO2', 'N/A')}%"
        )

        c3.metric(
            "🌡️ Body Temperature",
            f"{reading.get('Temperature', 'N/A')} °C"
        )

        c4, c5, c6 = st.columns(3)

        c4.metric(
            "🧠 Stress Level",
            f"{reading.get('Stress', 'N/A')}/100"
        )

        c5.metric(
            "🏃 Activity Level",
            f"{reading.get('Activity', 'N/A')}/100"
        )

        c6.metric(
            "😴 Sleep Duration",
            f"{reading.get('Sleep', 'N/A')} hours"
        )

    else:

        st.info("Start monitoring to display current health readings.")

    # ---------------------------------
    # ALERT SYSTEM
    # ---------------------------------

        st.markdown("### 🚨 Health Monitoring Alerts")

    if reading:

        alerts = []

        if reading.get("Heart Rate", 0) > 100:
            alerts.append("Heart rate is above the demo threshold.")

        if reading.get("SpO2", 100) < 95:
            alerts.append("Blood oxygen is below the demo threshold.")

        if reading.get("Temperature", 0) > 37.5:
            alerts.append("Temperature is above the demo threshold.")

        if reading.get("Stress", 0) > 75:
            alerts.append("Stress score is high.")

        if alerts:

            for alert in alerts:
                st.error("⚠️ " + alert)

        else:
            st.success("No demo threshold alerts at this moment.")

    else:

        st.info("Start monitoring to view health alerts.")
    # ---------------------------------
    # LIVE GRAPH
    # ---------------------------------

    if st.session_state.live_data:

        df = pd.DataFrame(st.session_state.live_data)

        st.markdown("### 📈 Live Heart Rate Monitoring")

        fig = px.line(
            df,
            x="Time",
            y="Heart Rate",
            markers=True,
            title="Heart Rate Changes Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            "The graph displays simulated readings, not actual "
            "astronaut measurements."
        )


live_dashboard()


# ---------------------------------
# HEALTH TRENDS
# ---------------------------------

st.markdown("---")

st.header("📊 Health Trends")

if st.session_state.live_data:

    df = pd.DataFrame(st.session_state.live_data)

    selected_parameter = st.selectbox(
        "Select Health Parameter",
        [
            "Heart Rate",
            "SpO2",
            "Temperature",
            "Stress",
            "Activity"
        ]
    )

    fig = px.line(
        df,
        x="Time",
        y=selected_parameter,
        markers=True,
        title=f"{selected_parameter} Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("Average:", round(df[selected_parameter].mean(), 2))
    st.write("Minimum:", round(df[selected_parameter].min(), 2))
    st.write("Maximum:", round(df[selected_parameter].max(), 2))

else:

    st.info(
        "Start live monitoring to generate health trend data."
    )


# ---------------------------------
# DATA EXPLORER
# ---------------------------------

st.markdown("---")

st.header("📁 Data Explorer")

uploaded_file = st.file_uploader(
    "Upload astronaut health data (CSV)",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        uploaded_df = pd.read_csv(uploaded_file)

        st.success("CSV file uploaded successfully!")

        st.dataframe(
            uploaded_df,
            use_container_width=True
        )

    except Exception as error:

        st.error(f"Unable to read CSV: {error}")


if st.session_state.live_data:

    live_df = pd.DataFrame(st.session_state.live_data)

    st.subheader("Generated Live Data")

    st.dataframe(
        live_df,
        use_container_width=True
    )

    csv_data = live_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Live Health Data",
        data=csv_data,
        file_name="astrocare_live_data.csv",
        mime="text/csv"
    )
        # PDF Health Report

    from io import BytesIO

    pdf_buffer = BytesIO()

    pdf = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    report_content = []

    report_content.append(
        Paragraph("ASTROCARE - Astronaut Health Report", styles["Title"])
    )

    report_content.append(Spacer(1, 20))

    report_content.append(
        Paragraph(f"Astronaut ID: {astronaut_id}", styles["Normal"])
    )

    report_content.append(
        Paragraph(
            f"Report Date: {pd.Timestamp.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    report_content.append(Spacer(1, 20))

    report_data = [["Health Parameter", "Recorded Value"]]

    for column in ["Heart Rate", "SpO2", "Temperature", "Stress", "Activity", "Sleep"]:

        if column in live_df.columns:

            report_data.append([
                column,
                str(live_df[column].iloc[-1])
            ])

    report_table = Table(report_data)

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    report_content.append(report_table)

    pdf.build(report_content)

    st.download_button(
        "📄 Download Astronaut Health Report (PDF)",
        data=pdf_buffer.getvalue(),
        file_name="astrocare_health_report.pdf",
        mime="application/pdf"
    )


# ---------------------------------
# ABOUT PROJECT
# ---------------------------------

# ---------------------------------
# MISSION HEALTH REPORT GENERATOR
# ---------------------------------

st.markdown("---")

st.header("📄 Mission Health Report")

st.write(
    "Generate a downloadable health report "
    "for the selected astronaut."
)


def generate_pdf_report():

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = []

    # Report Title
    content.append(
        Paragraph(
            "<b>ASTROCARE - MISSION HEALTH REPORT</b>",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    # Astronaut Profile
    content.append(
        Paragraph("<b>1. Astronaut Profile</b>", styles["Heading2"])
    )

    profile_data = [
        ["Parameter", "Details"],
        ["Astronaut Name", str(astronaut_name)],
        ["Astronaut ID", str(astronaut_id)],
        ["Mission", str(mission_name)],
        ["Crew Role", str(crew_role)],
        ["Report Date", datetime.now().strftime("%d-%m-%Y %H:%M")]
    ]

    profile_table = Table(profile_data)

    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(profile_table)

    content.append(Spacer(1, 20))

    # Health Summary
    content.append(
        Paragraph("<b>2. Latest Health Readings</b>", styles["Heading2"])
    )

    reading = st.session_state.current_reading

    health_data = [
        ["Health Parameter", "Latest Reading"],
        ["Heart Rate", f"{reading['Heart Rate']} BPM"],
        ["SpO2", f"{reading['SpO2']} %"],
        ["Temperature", f"{reading['Temperature']} °C"],
        ["Stress", str(reading["Stress"])],
        ["Activity", str(reading["Activity"])],
        ["Sleep", f"{reading['Sleep']} hours"]
    ]

    health_table = Table(health_data)

    health_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(health_table)

    content.append(Spacer(1, 20))

    # Historical Statistics
    content.append(
        Paragraph("<b>3. Historical Health Statistics</b>", styles["Heading2"])
    )

    history = st.session_state.live_data

    if history:

        history_df = pd.DataFrame(history)

        statistics_data = [
            ["Parameter", "Average", "Minimum", "Maximum"]
        ]

        for parameter in [
            "Heart Rate",
            "SpO2",
            "Temperature",
            "Stress",
            "Activity"
        ]:

            statistics_data.append([
                parameter,
                round(history_df[parameter].mean(), 2),
                round(history_df[parameter].min(), 2),
                round(history_df[parameter].max(), 2)
            ])

        statistics_table = Table(statistics_data)

        statistics_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ]))

        content.append(statistics_table)

    else:

        content.append(
            Paragraph(
                "No historical readings available.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 20))

    # Mental Wellness
    content.append(
        Paragraph("<b>4. Mental Wellness Records</b>", styles["Heading2"])
    )

    wellness_history = st.session_state.get(
        "wellness_history", []
    )

    if wellness_history:

        wellness_df = pd.DataFrame(wellness_history)

        wellness_data = [
            ["Date", "Mood", "Mood Score", "Stress"]
        ]

        for _, row in wellness_df.iterrows():

            wellness_data.append([
                str(row["Date"])[:16],
                str(row["Mood"]),
                str(row["Mood Score"]),
                str(row["Stress Level"])
            ])

        wellness_table = Table(
            wellness_data,
            repeatRows=1
        )

        wellness_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ]))

        content.append(wellness_table)

    else:

        content.append(
            Paragraph(
                "No mental wellness records available.",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<b>Note:</b> This report is generated using "
            "simulated health readings and self-reported "
            "wellness information. It is an educational "
            "prototype and not a medical diagnosis.",
            styles["Normal"]
        )
    )

    pdf.build(content)

    buffer.seek(0)

    return buffer.getvalue()


# Generate PDF Button

if st.button("📄 Generate Mission Health Report"):

    pdf_file = generate_pdf_report()

    st.success("Mission Health Report generated successfully!")

    st.download_button(
        label="⬇ Download ASTROCARE Health Report",
        data=pdf_file,
        file_name=f"ASTROCARE_{astronaut_id}_Health_Report.pdf",
        mime="application/pdf"
    )
# ---------------------------------
# MENTAL HEALTH & STRESS MONITORING
# ---------------------------------

st.markdown("---")

st.header("🧠 Mental Wellness Dashboard")

st.write(
    "Monitor astronaut mood, perceived stress "
    "and mental wellness during space missions."
)

# ---------------------------------
# MOOD TRACKING
# ---------------------------------

st.subheader("😊 Daily Mood Assessment")

mood = st.selectbox(
    "How is the astronaut feeling today?",
    [
        "Very Happy",
        "Happy",
        "Neutral",
        "Stressed",
        "Anxious",
        "Sad"
    ]
)

mood_score = {
    "Very Happy": 5,
    "Happy": 4,
    "Neutral": 3,
    "Stressed": 2,
    "Anxious": 1,
    "Sad": 1
}

selected_mood_score = mood_score[mood]

st.metric(
    "Mood Score",
    f"{selected_mood_score}/5"
)

# ---------------------------------
# STRESS ASSESSMENT
# ---------------------------------

st.subheader("📊 Stress Assessment")

stress_level = st.slider(
    "Select perceived stress level",
    min_value=0,
    max_value=100,
    value=25,
    help="0 = No perceived stress, 100 = Extremely high perceived stress"
)

st.metric(
    "Reported Stress Level",
    f"{stress_level}/100"
)

# ---------------------------------
# WELLNESS STATUS
# ---------------------------------

st.subheader("🩺 Mental Wellness Indicator")

if stress_level >= 75:

    st.error(
        "High reported stress. Consider additional rest "
        "and support from the mission's health team."
    )

elif stress_level >= 50:

    st.warning(
        "Moderately elevated reported stress. "
        "Monitor changes over time."
    )

else:

    st.success(
        "Reported stress is relatively low."
    )

# ---------------------------------
# WELLNESS SUGGESTIONS
# ---------------------------------

st.subheader("💡 Wellness Recommendations")

if stress_level >= 75:

    st.info(
        "Suggestion: Consider a relaxation break, "
        "guided breathing and communication with the "
        "mission support team."
    )

elif stress_level >= 50:

    st.info(
        "Suggestion: Consider a short break, "
        "relaxation exercises and a regular sleep schedule."
    )

elif mood in ["Sad", "Anxious", "Stressed"]:

    st.info(
        "Suggestion: Consider discussing emotional "
        "wellbeing with the mission support team."
    )

else:

    st.info(
        "Suggestion: Maintain regular sleep, "
        "physical activity and social communication."
    )

# ---------------------------------
# MOOD AND STRESS HISTORY
# ---------------------------------

st.subheader("📈 Mental Wellness History")

if "wellness_history" not in st.session_state:

    st.session_state.wellness_history = []

if st.button("Save Daily Wellness Record"):

    st.session_state.wellness_history.append({
        "Date": datetime.now(),
        "Mood": mood,
        "Mood Score": selected_mood_score,
        "Stress Level": stress_level
    })

    st.success("Wellness record saved successfully!")

if st.session_state.wellness_history:

    wellness_df = pd.DataFrame(
        st.session_state.wellness_history
    )

    st.dataframe(
        wellness_df,
        use_container_width=True
    )

    fig_wellness = px.line(
        wellness_df,
        x="Date",
        y="Stress Level",
        markers=True,
        title="Reported Stress History"
    )

    st.plotly_chart(
        fig_wellness,
        use_container_width=True
    )

    csv_wellness = wellness_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇ Download Wellness History",
        data=csv_wellness,
        file_name="astrocare_wellness_history.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No wellness records yet. Save a daily record "
        "to begin tracking mental wellness."
    )

st.caption(
    "Mental wellness indicators are based on self-reported "
    "information. They are not psychological diagnoses."
)

# ---------------------------------
# HISTORICAL HEALTH ANALYSIS
# ---------------------------------


st.markdown("---")

st.header("📊 Historical Health Analysis")

st.write(
    "Analyse the astronaut's recorded health readings "
    "throughout the mission."
)

if len(st.session_state.live_data) > 0:

    history_df = pd.DataFrame(st.session_state.live_data)

    st.subheader("📈 Select Health Parameter")

    selected_parameter = st.selectbox(
        "Choose a parameter for historical analysis",
        [
            "Heart Rate",
            "SpO2",
            "Temperature",
            "Stress",
            "Activity"
        ],
        key="historical_parameter"
    )

    fig_history = px.line(
        history_df,
        x="Time",
        y=selected_parameter,
        markers=True,
        title=f"{selected_parameter} History"
    )

    st.plotly_chart(
        fig_history,
        use_container_width=True
    )

    st.subheader("📋 Health Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average",
            round(history_df[selected_parameter].mean(), 2)
        )

    with col2:
        st.metric(
            "Minimum",
            round(history_df[selected_parameter].min(), 2)
        )

    with col3:
        st.metric(
            "Maximum",
            round(history_df[selected_parameter].max(), 2)
        )

else:

    st.info(
        "No historical health readings available. "
        "Start live monitoring to collect data."
    )

st.caption(
    "Historical analysis uses simulated health readings "
    "collected during the current application session."
)

# ---------------------------------
# SLEEP & CIRCADIAN RHYTHM ANALYSIS
# ---------------------------------

st.markdown("---")

st.header("😴 Sleep & Circadian Health")

st.write(
    "Monitor astronaut sleep duration, "
    "sleep consistency and estimated sleep quality."
)

# Sleep information

col1, col2, col3 = st.columns(3)

with col1:
    sleep_hours = st.number_input(
        "Sleep Duration (hours)",
        min_value=0.0,
        max_value=24.0,
        value=7.5,
        step=0.5
    )

with col2:
    sleep_start = st.time_input(
        "Sleep Start Time",
        value=datetime.strptime("22:00", "%H:%M").time()
    )

with col3:
    sleep_end = st.time_input(
        "Wake-up Time",
        value=datetime.strptime("06:00", "%H:%M").time()
    )

# Sleep quality estimation

if sleep_hours >= 7:

    sleep_quality = "Good"

elif sleep_hours >= 6:

    sleep_quality = "Moderate"

else:

    sleep_quality = "Insufficient"

# Display sleep information

st.markdown("### 💤 Sleep Summary")

c1, c2 = st.columns(2)

c1.metric(
    "Sleep Duration",
    f"{sleep_hours} hours"
)

c2.metric(
    "Estimated Sleep Quality",
    sleep_quality
)

# Sleep alerts

st.markdown("### 🚨 Sleep Monitoring")

if sleep_hours < 6:

    st.warning(
        "Insufficient sleep duration recorded. "
        "Consider reviewing the astronaut's sleep schedule."
    )

elif sleep_hours < 7:

    st.info(
        "Sleep duration is below the target used in this demonstration."
    )

else:

    st.success(
        "Sleep duration meets the demonstration target."
    )

# Sleep schedule information

st.markdown("### 🕒 Sleep Schedule")

st.write("Sleep started at:", sleep_start)

st.write("Wake-up time:", sleep_end)

# Sleep and stress relationship

if st.session_state.live_data:

    sleep_df = pd.DataFrame(
        st.session_state.live_data
    )

    sleep_df["Sleep Duration"] = sleep_hours

    st.markdown("### 🧠 Sleep and Stress Relationship")

    fig_sleep = px.scatter(
        sleep_df,
        x="Sleep Duration",
        y="Stress",
        title="Sleep Duration vs Stress Level",
        labels={
            "Sleep Duration": "Sleep Duration (hours)",
            "Stress": "Stress Score"
        }
    )

    st.plotly_chart(
        fig_sleep,
        use_container_width=True
    )

# Sleep History Tracking

# Sleep History Tracking

st.markdown("### 📅 Sleep History Tracking")

# Load previously saved records
if "sleep_history" not in st.session_state:

    try:
        old_history = pd.read_csv("sleep_history.csv")
        st.session_state.sleep_history = old_history.to_dict("records")

    except FileNotFoundError:
        st.session_state.sleep_history = []

# Save a new record
if st.button("Save Today's Sleep Record"):

    new_record = {
        "Date": pd.Timestamp.now().strftime("%d-%m-%Y %H:%M"),
        "Sleep Duration": sleep_hours,
        "Sleep Quality": sleep_quality
    }

    st.session_state.sleep_history.append(new_record)

    # Save records permanently
    history_df = pd.DataFrame(st.session_state.sleep_history)
    history_df.to_csv("sleep_history.csv", index=False)

    st.success("Sleep record saved permanently!")

# Display sleep history
if st.session_state.sleep_history:

    history_df = pd.DataFrame(st.session_state.sleep_history)

    st.markdown("#### 📈 Sleep Duration History")

    st.line_chart(
        history_df.set_index("Date")["Sleep Duration"]
    )

    st.markdown("#### 📋 Recorded Sleep Details")

    st.dataframe(history_df, use_container_width=True)

else:
    st.info("No sleep history available. Save your first record.")
st.caption(
    "Sleep quality is an illustrative estimate based on duration. "
    "It is not a clinical sleep assessment."
)

st.markdown("---")

st.header("ℹ️ About ASTROCARE")

st.write("""
ASTROCARE is an astronaut health-monitoring software prototype.

Its objectives include:

- Monitoring important health parameters.
- Observing changes in health readings.
- Identifying unusual readings using demo thresholds.
- Analysing health trends.
- Supporting astronaut health-data visualisation.

The current version uses simulated data for demonstration.
It is not a medical diagnostic system or a validated
astronaut emergency-warning system.
""")

st.caption(
    "ASTROCARE | Astronaut Health Monitoring Prototype"
)

# ---------------------------------
# NASA BLOOD SERUM DATASET
# ---------------------------------

from pathlib import Path

st.markdown("---")

st.header("🧪 NASA Historical Blood Serum Analysis")

st.write(
    "Explore historical blood serum measurements "
    "from the NASA Open Science Data Repository."
)

data_folder = Path(__file__).parent / "data"

csv_files = list(data_folder.glob("*.csv"))

transformed_files = [
    file for file in csv_files
    if "TRANSFORMED" in file.name.upper()
]

if transformed_files:

    nasa_df = pd.read_csv(transformed_files[0])

    st.success("NASA dataset loaded successfully!")

    st.write("Dataset shape:", nasa_df.shape)

    st.subheader("Dataset Preview")

    st.dataframe(nasa_df.head(10), use_container_width=True)

    st.subheader("Available Parameters")

    st.write(list(nasa_df.columns))

    # Individual sample selection
    st.subheader("🔬 Individual Serum Sample Analysis")

    sample_column = next(
        (col for col in nasa_df.columns
         if col.strip().lower() == "sample name"),
        None
    )

    if sample_column is not None:

        sample_names = nasa_df[sample_column].dropna().unique()

        selected_sample = st.selectbox(
            "Select a Serum Sample",
            sample_names
        )

        sample_data = nasa_df[
            nasa_df[sample_column] == selected_sample
        ]

        st.write("Selected Sample:", selected_sample)

        st.dataframe(sample_data, use_container_width=True)
                # NASA Blood Parameter Visualization

        st.markdown("---")
        st.subheader("📊 Blood Parameter Visualization")

        numeric_columns = nasa_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        # Exclude reference range columns
        parameters = [
            col for col in numeric_columns
            if "range" not in col.lower()
            and "min" not in col.lower()
            and "max" not in col.lower()
        ]

        if parameters:

            selected_parameter = st.selectbox(
                "Choose a Blood Parameter",
                parameters
            )

            chart_data = nasa_df[
                [sample_column, selected_parameter]
            ].copy()

            chart_data[selected_parameter] = pd.to_numeric(
                chart_data[selected_parameter],
                errors="coerce"
            )

            chart_data = chart_data.dropna()

            fig = px.bar(
                chart_data,
                x=sample_column,
                y=selected_parameter,
                title=f"{selected_parameter} Across Serum Samples"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric blood parameters found.")
                    # Blood Reference Range Analysis

        st.markdown("---")
        st.subheader("🩸 Blood Reference Range Analysis")

        value_columns = [
            col for col in nasa_df.columns
            if "_value_" in col.lower()
        ]

        available_tests = []

        for col in value_columns:
            min_col = col.lower().replace("_value_", "_range_min_")
            max_col = col.lower().replace("_value_", "_range_max_")

            matching_min = next(
                (c for c in nasa_df.columns if c.lower() == min_col),
                None
            )

            matching_max = next(
                (c for c in nasa_df.columns if c.lower() == max_col),
                None
            )

            if matching_min and matching_max:
                available_tests.append((col, matching_min, matching_max))

        if available_tests:

            test_names = [test[0] for test in available_tests]

            selected_test = st.selectbox(
                "Select a Blood Test for Range Analysis",
                test_names
            )

            value_col, min_col, max_col = next(
                test for test in available_tests
                if test[0] == selected_test
            )

            test_row = sample_data.iloc[0]

            value = pd.to_numeric(test_row[value_col], errors="coerce")
            minimum = pd.to_numeric(test_row[min_col], errors="coerce")
            maximum = pd.to_numeric(test_row[max_col], errors="coerce")

            st.write("Selected Test:", selected_test)

            if pd.notna(value) and pd.notna(minimum) and pd.notna(maximum):

                st.metric("Measured Value", f"{value:.2f}")
                st.write(f"Minimum Reference Value: {minimum}")
                st.write(f"Maximum Reference Value: {maximum}")

                if value < minimum:
                    st.warning("Below the provided reference range.")

                elif value > maximum:
                    st.warning("Above the provided reference range.")

                else:
                    st.success("Within the provided reference range.")

            else:
                st.info("Complete measurement or reference range data is unavailable for this sample.")

        else:
            st.warning("Matching blood test reference ranges were not found.")
                    # HEALTH RISK SUMMARY

        st.markdown("---")
        st.subheader("🩺 Astronaut Health Summary")

        summary_results = []

        selected_row = sample_data.iloc[0]

        for value_col, min_col, max_col in available_tests:

            value = pd.to_numeric(
                selected_row[value_col], errors="coerce"
            )

            minimum = pd.to_numeric(
                selected_row[min_col], errors="coerce"
            )

            maximum = pd.to_numeric(
                selected_row[max_col], errors="coerce"
            )

            if pd.notna(value) and pd.notna(minimum) and pd.notna(maximum):

                if value < minimum:
                    status = "Below Range"

                elif value > maximum:
                    status = "Above Range"

                else:
                    status = "Within Range"

                summary_results.append({
                    "Blood Parameter": value_col,
                    "Measured Value": value,
                    "Minimum": minimum,
                    "Maximum": maximum,
                    "Status": status
                })

        if summary_results:

            summary_df = pd.DataFrame(summary_results)

            total = len(summary_df)
            within = (summary_df["Status"] == "Within Range").sum()
            below = (summary_df["Status"] == "Below Range").sum()
            above = (summary_df["Status"] == "Above Range").sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Analysed", total)
            col2.metric("Within Range", within)
            col3.metric("Below Range", below)
            col4.metric("Above Range", above)

            st.subheader("Detailed Health Summary")

            st.dataframe(
                summary_df,
                use_container_width=True
            )

        else:
            st.info("No complete blood measurements available for summary.")

        # ---------------------------------
        # STAGE 8: HISTORICAL BLOOD COMPARISON
        # ---------------------------------

        st.markdown("---")
        st.subheader("📈 Historical Blood Measurement Comparison")

        historical_df = nasa_df.copy()

        historical_df[sample_column] = (
            historical_df[sample_column].astype(str).str.strip()
        )

        historical_df["Participant ID"] = (
            historical_df[sample_column]
            .str.split("_serum_", n=1).str[0]
        )

        participant_ids = sorted(
            historical_df.loc[
                historical_df[sample_column].str.contains(
                    "_serum_", case=False, na=False
                ),
                "Participant ID"
            ].dropna().unique()
        )

        historical_value_columns = [
            col for col in nasa_df.columns
            if "_value_" in col.lower()
        ]

        if participant_ids and historical_value_columns:

            chosen_participant = st.selectbox(
                "Select Participant for Historical Comparison",
                participant_ids
            )

            chosen_value_col = st.selectbox(
                "Select Blood Parameter for Comparison",
                historical_value_columns,
                key="historical_parameter_select"
            )

            participant_data = historical_df[
                historical_df["Participant ID"] == chosen_participant
            ].copy()

            participant_data[chosen_value_col] = pd.to_numeric(
                participant_data[chosen_value_col],
                errors="coerce"
            )

            participant_data = participant_data.dropna(
                subset=[chosen_value_col]
            )

            if not participant_data.empty:

                fig_history = px.line(
                    participant_data,
                    x=sample_column,
                    y=chosen_value_col,
                    markers=True,
                    title=f"{chosen_value_col} across available samples for {chosen_participant}"
                )

                st.plotly_chart(
                    fig_history,
                    use_container_width=True
                )

                st.dataframe(
                    participant_data[
                        [sample_column, chosen_value_col]
                    ],
                    use_container_width=True
                )

            else:
                st.info(
                    "No numeric measurements are available for this participant and parameter."
                )

        else:
            st.warning(
                "Participant IDs or blood measurement columns were not found."
            )
                # ---------------------------------
        # STAGE 9: INTEGRATED HEALTH OVERVIEW
        # ---------------------------------

        st.markdown("---")
        st.header("🚀 Integrated Astronaut Health Overview")

        st.write(
            "A combined overview of the health monitoring "
            "and historical analysis modules in ASTROCARE."
        )

        # Live Health Monitoring
        st.subheader("❤️ Live Health Monitoring")

        current_reading = st.session_state.astronaut_current_readings.get(
            astronaut_id,
            st.session_state.get("current_reading", {})
        )

        if current_reading:
            st.success("Live monitoring data is available.")
            st.json(current_reading)
        else:
            st.info(
                "Start Live Health Monitoring to view current readings."
            )

                # Overall Astronaut Health Summary

        st.subheader("📊 Overall Astronaut Health Summary")

        if current_reading:

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "❤️ Heart Rate",
                f"{current_reading.get('Heart Rate', 'N/A')} bpm"
            )

            c2.metric(
                "🩸 Oxygen Saturation",
                f"{current_reading.get('SpO2', 'N/A')}%"
            )

            c3.metric(
                "🌡️ Temperature",
                f"{current_reading.get('Temperature', 'N/A')} °C"
            )

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "🧠 Stress",
                current_reading.get("Stress", "N/A")
            )

            c5.metric(
                "🏃 Activity",
                current_reading.get("Activity", "N/A")
            )

            c6.metric(
                "💤 Sleep",
                f"{current_reading.get('Sleep', 'N/A')} hours"
            )

        else:

            st.info("Health readings are not available yet.")


        # Health Trend Visualization

        st.subheader("📈 Astronaut Health Trends")

        health_history = st.session_state.astronaut_health_data.get(
            astronaut_id, []
        )

        if health_history:

            trend_df = pd.DataFrame(health_history)

            available_metrics = [
                col for col in ["Heart Rate", "SpO2", "Temperature", "Stress"]
                if col in trend_df.columns
            ]

            if available_metrics:

                selected_metric = st.selectbox(
                    "Select health parameter",
                    available_metrics
                )

                st.line_chart(trend_df[selected_metric])

            else:
                st.info("No suitable health measurements available.")

        else:
            st.info("Generate live readings to view health trends.")

        # AI Anomaly Detection
        st.subheader("🤖 AI Anomaly Detection")

        st.write(
            "The AI module analyses simulated health readings "
            "to identify unusual patterns."
        )

                # Sleep Analysis
        st.subheader("😴 Sleep Analysis")

        st.write(
            "Displays astronaut sleep information "
            "and previously recorded sleep history."
        )

        try:
            sleep_df = pd.read_csv("sleep_history.csv")

            if not sleep_df.empty:

                st.success("Sleep history loaded successfully.")

                st.metric(
                    "Latest Sleep Duration",
                    f"{sleep_df.iloc[-1]['Sleep Duration']} hours"
                )

                st.markdown("#### 📈 Sleep Duration Trend")

                st.line_chart(
                    sleep_df.set_index("Date")["Sleep Duration"]
                )

                st.markdown("#### 📋 Sleep Records")

                st.dataframe(
                    sleep_df,
                    use_container_width=True
                )

            else:
                st.info("No sleep records available.")

        except FileNotFoundError:
            st.info("No sleep history file found yet.")

        # Mental Wellness
        st.subheader("🧠 Mental Wellness")

        st.write(
            "Displays the mental wellness information "
            "available in the dashboard."
        )

        # NASA Blood Serum Analysis
        st.subheader("🧪 NASA Historical Blood Analysis")

        st.success("NASA historical serum dataset is loaded.")

        st.write("Selected Serum Sample:", selected_sample)

        if summary_results:
            st.write(
                "Number of blood parameters analysed:",
                len(summary_results)
            )
        else:
            st.info(
                "No complete blood measurements are available "
                "for the selected sample."
            )

        st.caption(
            "Note: Live readings are simulated. NASA blood serum "
            "measurements are historical research data. "
            "This overview is not a medical diagnosis."
        )

    else:
        st.error("Sample Name column was not found.")

else:

    st.warning(
        "Transformed NASA CSV file was not found "
        "inside the data folder."
    )