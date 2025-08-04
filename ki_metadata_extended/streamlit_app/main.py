import streamlit as st
import pandas as pd
import plotly.express as px

st.title("KI-Metadaten Timeline")

try:
    logs = open("/logs/analysis.log").readlines()
    entries = [eval(l.split(" - METADATA: ")[1]) for l in logs if "METADATA" in l]
    df = pd.DataFrame(entries)
    df['time'] = [l.split(" - ")[0] for l in logs if "METADATA" in l]
    fig = px.timeline(df, x_start='time', x_end='time', y='caption', color='face_info')
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"Keine Daten gefunden oder Fehler: {e}")
