import streamlit as st

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

# Dashboard content (only shown if logged in)
st.title("Dashboard")
st.success(f"Welcome, {st.session_state.username}!")


st.header("Domain Overview")

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

st.header("Security Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Threats Detected", 247, delta="+12")

with col2:
    st.metric("Vulnerabilities", 8, delta="-3")

with col3:
    st.metric("Incidents", 3, delta="+1")


st.header("Incident Trends")

# Sample data for chart
import pandas as pd
import numpy as np

# Create sample data
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Malware', 'Phishing', 'DDoS']
)

# Line chart 
st.line_chart(data)

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