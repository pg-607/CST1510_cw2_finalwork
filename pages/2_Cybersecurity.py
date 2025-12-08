import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    layout="wide"
)

from app.auth import initialize_session_state

# Initialize session
initialize_session_state()

# Authentication check
if not st.session_state.logged_in:
    st.error("🚫 You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()
# Title
st.title("🔒 Cybersecurity Dashboard")

# Security metrics from PDF page 20
st.header("Security Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Threats Detected", 247, delta="+12")

with col2:
    st.metric("Vulnerabilities", 8, delta="-3")

with col3:
    st.metric("Incidents", 3, delta="+1")

# Threat distribution 
st.header("Threat Distribution")

# Data 
threat_data = pd.DataFrame({
    "Threat Type": ["Malware", "Phishing", "DDoS", "Intrusion"],
    "Count": [89, 67, 45, 46]
})

# Bar chart 
st.bar_chart(threat_data.set_index("Threat Type"))

# Incident trends
st.header("Incident Trends Over Time")

# Create sample time series data
dates = pd.date_range(start="2024-01-01", end="2024-11-01", freq="D")
trend_data = pd.DataFrame({
    "Date": dates,
    "Incidents": np.random.randint(0, 10, size=len(dates))
})

# Line chart 
st.line_chart(trend_data.set_index("Date"))

# CRUD Operations 
st.header("Incident Management")

# CREATE form 
with st.form("add_incident"):
    st.subheader("Report New Incident")
    
    incident_type = st.selectbox(
        "Incident Type",
        ["Malware", "Phishing", "DDoS", "Unauthorized Access", "Data Breach"]
    )
    
    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )
    
    description = st.text_area("Description")
    
    submitted = st.form_submit_button("Add Incident")
    
    if submitted:
        # Initialize records list if not present
        if "incidents" not in st.session_state:
            st.session_state.incidents = []
        
        # Add new record
        record = {
            "type": incident_type,
            "severity": severity,
            "description": description,
            "status": "Open"
        }
        st.session_state.incidents.append(record)
        st.success("Incident added!")

# READ - Display incidents 
st.header("All Incidents")

if "incidents" in st.session_state and st.session_state.incidents:
    # Convert to DataFrame 
    df = pd.DataFrame(st.session_state.incidents)
    
    # Display interactive table 
    st.dataframe(df, use_container_width=True)
    
    # UPDATE - Modify incidents 
    st.subheader("Update Incident Status")
    
    # Get incident names for selection
    incident_names = [f"Incident {i+1}: {inc['type']}" for i, inc in enumerate(st.session_state.incidents)]
    
    if incident_names:
        selected = st.selectbox("Select incident to update", incident_names)
        
        # Find index
        idx = incident_names.index(selected)
        incident = st.session_state.incidents[idx]
        
        # Update form (PDF page 19)
        with st.form("update_form"):
            new_status = st.selectbox(
                "New Status",
                ["Open", "Investigating", "Resolved", "Closed"],
                index=["Open", "Investigating", "Resolved", "Closed"].index(incident["status"])
            )
            
            if st.form_submit_button("Update"):
                st.session_state.incidents[idx]["status"] = new_status
                st.success("Record updated!")
                st.rerun()
        
        # DELETE - Remove incidents 
        st.subheader("Delete Incident")
        
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning(f"Delete {selected}?")
        
        with col2:
            if st.button("Delete", type="primary"):
                st.session_state.incidents.pop(idx)
                st.success("Record deleted!")
                st.rerun()
else:
    st.info("No incidents found")

# Navigation
st.markdown("---")
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

# AI Assistant Integration (Week 10)
st.markdown("---")
if st.button(f"Ask AI Assistant", use_container_width=True):
    st.switch_page("pages/6_AI_Assistant.py")