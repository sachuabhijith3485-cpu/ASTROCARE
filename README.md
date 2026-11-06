# ASTROCARE – Astronaut Health Monitoring System

**Team Name: ASTRIONYX**

ASTROCARE is a Streamlit-based astronaut health monitoring and analysis prototype developed for the NASA Space Apps Challenge 2026.

Our goal is to demonstrate how health monitoring, machine learning, data visualization and historical health data analysis can be combined in one platform to support astronaut health management.

## Key Features

- Live simulated astronaut health monitoring.
- AI-based anomaly detection using Isolation Forest.
- Multiple astronaut profiles with separate health histories.
- Sleep monitoring and sleep history tracking.
- Mental wellness monitoring module.
- NASA historical blood serum data analysis.
- Blood reference range comparison.
- Participant historical blood measurement visualization.
- Integrated astronaut health overview.
- Health trend visualization.
- CSV and PDF health report downloads.

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- ReportLab

## Historical Blood Dataset

ASTROCARE uses historical blood serum measurements from NASA's Open Science Data Repository (OSDR).

Study: OSD-575

The dataset is used to demonstrate historical blood parameter visualization and reference range comparison.

## How to Run

1. Install Python.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install the required libraries:

   pip install -r requirements.txt

5. Run the application:

   python -m streamlit run app.py

6. Open the local Streamlit application in your browser.

## Project Limitations

- Live astronaut health readings are simulated.
- The application is not connected to real astronaut sensors.
- Historical blood measurements are not live measurements.
- Sleep information is illustrative and not obtained from clinical sleep monitoring equipment.
- AI anomaly detection is a demonstration feature.
- The application is not a medical device and does not provide medical diagnosis or emergency advice.

## Project Team

Team Name: ASTRIONYX

Project Name: ASTROCARE

NASA Space Apps Challenge 2026