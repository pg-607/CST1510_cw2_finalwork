import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="IT Operations Dashboard",
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
st.title("🖥️ IT Operations Dashboard")

# System health metrics 
st.header("System Health")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", "42%", delta="+3%")

with col2:
    st.metric("Memory", "63%", delta="-0.5%")

with col3:
    st.metric("Disk", "81%", delta="+1.5%")

# Ticket management
st.header("Ticket Management")

# Sample ticket data
tickets = pd.DataFrame({
    "Ticket ID": [1001, 1002, 1003, 1004, 1005],
    "Priority": ["High", "Medium", "Low", "High", "Medium"],
    "Status": ["Open", "In Progress", "Resolved", "Open", "Closed"],
    "Category": ["Hardware", "Software", "Network", "Software", "Hardware"],
    "Created": ["2024-11-01", "2024-11-02", "2024-10-30", "2024-11-03", "2024-10-29"],
    "Assignee": ["Alice", "Bob", "Charlie", "Alice", "Bob"]
})

# Display tickets
st.dataframe(tickets, use_container_width=True)

# Ticket statistics
st.header("Ticket Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    open_tickets = len(tickets[tickets["Status"] == "Open"])
    st.metric("Open", open_tickets)

with col2:
    high_priority = len(tickets[tickets["Priority"] == "High"])
    st.metric("High Priority", high_priority)

with col3:
    avg_resolution = "2.5 days"
    st.metric("Avg Resolution", avg_resolution)

with col4:
    sla_compliance = "94%"
    st.metric("SLA Compliance", sla_compliance)

# Resource usage over time
st.header("Resource Usage Over Time")

# Create time series data
dates = pd.date_range(start="2024-11-01", periods=24, freq="H")
usage_data = pd.DataFrame({
    "Time": dates,
    "CPU": np.random.randint(30, 80, size=24),
    "Memory": np.random.randint(50, 90, size=24),
    "Network": np.random.randint(20, 70, size=24)
})

# Line chart for resource usage
st.line_chart(usage_data.set_index("Time"))

# Service status
st.header("Service Status")

services = pd.DataFrame({
    "Service": ["Web Server", "Database", "API Gateway", "Cache", "Message Queue"],
    "Status": ["✅ Healthy", "✅ Healthy", "⚠️ Degraded", "✅ Healthy", "✅ Healthy"],
    "Uptime": ["99.9%", "99.95%", "99.8%", "99.99%", "99.9%"],
    "Response Time": ["45ms", "120ms", "85ms", "12ms", "25ms"]
})

st.dataframe(services, use_container_width=True)

# Navigation
st.markdown("---")
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

# AI Assistant Integration (Week 10)
st.markdown("---")
if st.button(f"Ask AI Assistant", use_container_width=True):
    st.switch_page("pages/6_AI_Assistant.py")