import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import ast

st.set_page_config(
    page_title="KI-Metadaten Timeline",
    page_icon="📊",
    layout="wide"
)

st.title("📊 KI-Metadaten Timeline")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("Einstellungen")
show_errors = st.sidebar.checkbox("Fehler anzeigen", value=False)
max_entries = st.sidebar.slider("Maximale Einträge", 10, 1000, 100)

@st.cache_data(ttl=60)  # Cache for 1 minute
def load_log_data():
    """Load and parse log data with error handling"""
    try:
        with open("/logs/analysis.log", "r") as f:
            logs = f.readlines()
        
        entries = []
        times = []
        
        for line in logs:
            if "METADATA" in line:
                try:
                    # Parse timestamp
                    time_str = line.split(" - METADATA: ")[0]
                    time_obj = datetime.fromisoformat(time_str)
                    times.append(time_obj)
                    
                    # Parse metadata
                    metadata_str = line.split(" - METADATA: ")[1].strip()
                    
                    # Try to parse as JSON first, then as Python literal
                    try:
                        metadata = json.loads(metadata_str)
                    except json.JSONDecodeError:
                        try:
                            metadata = ast.literal_eval(metadata_str)
                        except:
                            metadata = {"raw": metadata_str}
                    
                    entries.append(metadata)
                    
                except Exception as e:
                    if show_errors:
                        st.warning(f"Fehler beim Parsen der Zeile: {line[:100]}... - {e}")
                    continue
        
        return times, entries
    
    except FileNotFoundError:
        st.warning("Keine Log-Datei gefunden. Bitte laden Sie zuerst Bilder hoch.")
        return [], []
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return [], []

# Load data
times, entries = load_log_data()

if times and entries:
    # Create DataFrame
    df = pd.DataFrame(entries)
    df['timestamp'] = times
    df['date'] = df['timestamp'].dt.date
    df['time'] = df['timestamp'].dt.time
    
    # Limit entries
    df = df.tail(max_entries)
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Gesamt Einträge", len(df))
    with col2:
        st.metric("Eindeutige Captions", df['caption'].nunique() if 'caption' in df.columns else 0)
    with col3:
        st.metric("Erfolgreiche Analysen", len(df[df.get('face_info', {}).apply(lambda x: 'error' not in str(x))]))
    with col4:
        st.metric("Letzter Eintrag", df['timestamp'].max().strftime("%H:%M:%S") if len(df) > 0 else "N/A")
    
    st.markdown("---")
    
    # Timeline visualization
    st.subheader("📈 Timeline der Analysen")
    
    if 'caption' in df.columns:
        # Create timeline
        fig = px.timeline(
            df, 
            x_start='timestamp', 
            x_end='timestamp', 
            y='caption', 
            color='caption',
            title="Analyse Timeline"
        )
        fig.update_layout(
            xaxis_title="Zeit",
            yaxis_title="Caption",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Face analysis statistics
    st.subheader("👤 Gesichtsanalyse Statistiken")
    
    if 'face_info' in df.columns:
        # Extract age and gender data
        ages = []
        genders = []
        
        for face_info in df['face_info']:
            if isinstance(face_info, dict):
                if 'age' in face_info and face_info['age'] is not None:
                    ages.append(face_info['age'])
                if 'gender' in face_info and face_info['gender'] is not None:
                    genders.append(face_info['gender'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if ages:
                st.subheader("Altersverteilung")
                age_df = pd.DataFrame({'age': ages})
                fig_age = px.histogram(age_df, x='age', nbins=10, title="Altersverteilung")
                st.plotly_chart(fig_age, use_container_width=True)
            else:
                st.info("Keine Altersdaten verfügbar")
        
        with col2:
            if genders:
                st.subheader("Geschlechterverteilung")
                gender_df = pd.DataFrame({'gender': genders})
                gender_counts = gender_df['gender'].value_counts()
                fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, title="Geschlechterverteilung")
                st.plotly_chart(fig_gender, use_container_width=True)
            else:
                st.info("Keine Geschlechterdaten verfügbar")
    
    # Raw data table
    st.subheader("📋 Rohdaten")
    st.dataframe(df, use_container_width=True)
    
else:
    st.info("Keine Daten verfügbar. Bitte laden Sie zuerst Bilder über die API hoch.")
    
    st.markdown("---")
    st.subheader("📤 API Verwendung")
    st.code("""
# Beispiel für Bild-Upload
curl -X POST "http://localhost:8000/upload/" \\
     -H "accept: application/json" \\
     -H "Content-Type: multipart/form-data" \\
     -F "file=@your_image.jpg"
    """)
