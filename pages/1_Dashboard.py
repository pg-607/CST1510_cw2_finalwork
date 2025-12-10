import streamlit as st
import pandas as pd
from pathlib import Path

# Import OOP services
from services.database_manager import DatabaseManager
from services.incident_service import IncidentService

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Page configuration
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# Initialize session state (local helper — other pages define this same helper)
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None


# Initialize session
initialize_session_state()

# Authentication check
if not st.session_state.logged_in:
    st.error("🚫 You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Initialize services (OOP)
db = DatabaseManager(str(DB_PATH))
incident_service = IncidentService(db)

# Dashboard content (only shown if logged in)
st.title("Dashboard")
st.success(f"Welcome, {st.session_state.username}!")


st.header("Domain Overview")
# Navigation buttons to other dashboards
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Cybersecurity")
    if st.button("View Security Dashboard"):
        st.switch_page("pages/2_Cybersecurity.py")

with col2:
    st.subheader("Data Science")
    if st.button("View Data Analytics"):
        st.switch_page("pages/3_Data_Science.py")

with col3:
    st.subheader("IT Operations")
    if st.button("View IT Dashboard"):
        st.switch_page("pages/4_IT_Operations.py")
# Security metrics (placeholder)
st.header("Security Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Threats Detected", 247, delta="+12")

with col2:
    st.metric("Vulnerabilities", 8, delta="-3")

with col3:
    st.metric("Incidents", 3, delta="+1")

# show recent incidents
st.header("Incident Trends")

# Get actual incident data from database
incidents = incident_service.get_all_incidents()

if incidents:
    # Parse timestamps and count incidents by date
    dates = []
    for inc in incidents:
        try:
            timestamp = pd.to_datetime(inc.get_timestamp())
            dates.append(timestamp.date())
        except Exception:
            continue
    
    if dates:
        # Create a time series of incident counts by date
        ts = pd.Series(dates).value_counts().sort_index()
        df_incidents = ts.rename_axis('date').reset_index(name='count')
        df_incidents['date'] = pd.to_datetime(df_incidents['date'])
        
        # Display the line chart
        st.line_chart(df_incidents.set_index('date'))
        
        st.info(f"Showing incident activity from the last {len(df_incidents)} days")
    else:
        st.info("No incident data available for chart")
else:
    st.info("No incidents recorded yet")

# Sidebar with logout
with st.sidebar:
    st.header("User Controls")
    st.write(f"User: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role}")
    
    # Logout button 
    if st.button("Log out"):
        # Reset session state 
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.write("You have been logged out")
        st.switch_page("Home.py")

# AI Assistant Integration (Week 10)
st.markdown("---")
if st.button(f"Ask  AI Assistant", use_container_width=True):
    st.switch_page("pages/6_AI_Assistant.py")

# Close database connection when done
db.close()