"""
Refactored Cybersecurity Page - Using OOP with SecurityIncident and IncidentService
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Import OOP classes
from services.database_manager import DatabaseManager
from services.incident_service import IncidentService

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "role" not in st.session_state:
        st.session_state.role = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

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

# Title
st.title("🔒 Cybersecurity Dashboard")

# Get all incidents using the service
incidents = incident_service.get_all_incidents()

# Security metrics
st.header("Security Metrics")
col1, col2, col3 = st.columns(3)

# Calculate metrics from incident objects
open_count = len([i for i in incidents if i.get_status() == "Open"])
high_critical_count = len([i for i in incidents if i.get_severity() in ["High", "Critical"]])
resolved_count = len([i for i in incidents if i.get_status() == "Resolved"])

with col1:
    st.metric("Open Incidents", open_count)

with col2:
    st.metric("High/Critical", high_critical_count)

with col3:
    st.metric("Resolved", resolved_count)

# Threat distribution
st.header("Threat Distribution by Category")

# Get category counts using service
category_counts = incident_service.get_incident_count_by_category()

# Chart selector
st.subheader("Charts")
chart_type = st.selectbox(
    "Select chart type",
    [
        "Threat Distribution (Bar)",
        "Incident Trend (Line)",
        "Severity Breakdown (Pie)"
    ]
)

if chart_type == "Threat Distribution (Bar)":
    if category_counts:
        threat_data = pd.DataFrame({
            "Threat Type": list(category_counts.keys()),
            "Count": list(category_counts.values())
        })
        st.bar_chart(threat_data.set_index("Threat Type"))
    else:
        st.info("No threat data available")

elif chart_type == "Incident Trend (Line)":
    if incidents:
        # Build time series of incident counts by date
        dates = []
        for inc in incidents:
            try:
                dates.append(pd.to_datetime(inc.get_timestamp()).date())
            except Exception:
                # If timestamp not parseable, skip
                continue

        if dates:
            ts = pd.Series(dates).value_counts().sort_index()
            df_ts = ts.rename_axis('date').reset_index(name='count')
            df_ts['date'] = pd.to_datetime(df_ts['date'])
            st.line_chart(df_ts.set_index('date'))
        else:
            st.info("No timestamped incidents available for trend")
    else:
        st.info("No incidents found")

else:  # Severity Breakdown (Pie)
    if incidents:
        severity_counts = {}
        for inc in incidents:
            sev = inc.get_severity() or "Unknown"
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        if severity_counts:
            df_sev = pd.DataFrame({
                'Severity': list(severity_counts.keys()),
                'Count': list(severity_counts.values())
            })
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.pie(df_sev['Count'], labels=df_sev['Severity'], autopct='%1.1f%%')
            ax.set_title('Incidents by Severity')
            st.pyplot(fig)
        else:
            st.info("No severity data available")
    else:
        st.info("No incidents found")

# Display incidents table
st.header("Recent Security Incidents")

if incidents:
    # Convert incident objects to DataFrame for display
    incident_data = []
    for incident in incidents[:20]:  # Show first 20
        incident_data.append({
            'ID': incident.get_id(),
            'Type': incident.get_incident_type(),
            'Severity': incident.get_severity(),
            'Status': incident.get_status(),
            'Description': incident.get_description()[:50] + "...",
            'Timestamp': incident.get_timestamp()
        })
    
    df = pd.DataFrame(incident_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No incidents found")

# CRUD Operations
st.header("Incident Management")

# CREATE - Add new incident
with st.form("add_incident"):
    st.subheader("Report New Incident")
    
    incident_type = st.selectbox(
        "Incident Type",
        ["Malware", "Phishing", "DDoS", "Unauthorized Access", "Misconfiguration"]
    )
    
    severity = st.selectbox(
        "Severity",
        ["Low", "Medium", "High", "Critical"]
    )
    
    description = st.text_area("Description")
    
    submitted = st.form_submit_button("Add Incident")
    
    if submitted and description:
        # Use service to create incident
        new_id = incident_service.create_incident(
            incident_type=incident_type,
            severity=severity,
            description=description,
            reported_by=st.session_state.username
        )
        st.success(f"✅ Incident #{new_id} created successfully!")
        st.rerun()

# UPDATE - Modify incident status
st.subheader("Update Incident Status")

if incidents:
    # Create selection list
    incident_options = {
        f"Incident {i.get_id()}: {i.get_incident_type()} [{i.get_severity()}]": i
        for i in incidents[:10]
    }
    
    selected_key = st.selectbox("Select incident to update", list(incident_options.keys()))
    selected_incident = incident_options[selected_key]
    
    # Display current status
    st.write(f"Current Status: **{selected_incident.get_status()}**")
    
    # Update form
    with st.form("update_form"):
        new_status = st.selectbox(
            "New Status",
            ["Open", "In Progress", "Resolved", "Closed"],
            index=["Open", "In Progress", "Resolved", "Closed"].index(
                selected_incident.get_status()
            ) if selected_incident.get_status() in ["Open", "In Progress", "Resolved", "Closed"] else 0
        )
        
        if st.form_submit_button("Update Status"):
            # Use service to update
            success = incident_service.update_incident_status(
                selected_incident.get_id(),
                new_status
            )
            
            if success:
                st.success("✅ Incident status updated!")
                st.rerun()
            else:
                st.error("❌ Failed to update incident")
    
    # DELETE - Remove incident
    st.subheader("Delete Incident")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning(f"Delete {selected_key}?")
    
    with col2:
        if st.button("🗑️ Delete", type="primary"):
            success = incident_service.delete_incident(selected_incident.get_id())
            
            if success:
                st.success("✅ Incident deleted!")
                st.rerun()
            else:
                st.error("❌ Failed to delete incident")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    if st.button("🤖 Ask AI Assistant", use_container_width=True):
        st.switch_page("pages/6_AI_Assistant.py")

# Close database connection
db.close()