import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Science Dashboard",
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
st.title("📈 Data Science Dashboard")

# Model performance metrics
st.header("Model Performance")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Accuracy", "94.2%")

with col2:
    st.metric("Precision", "91.8%")

with col3:
    st.metric("Recall", "89.5%")

# Training history from PDF page 20
st.header("Training History")

# Create sample training data 
history = pd.DataFrame({
    "epoch": [1, 2, 3, 4, 5],
    "loss": [0.45, 0.32, 0.24, 0.18, 0.15],
    "accuracy": [0.78, 0.85, 0.89, 0.92, 0.94]
})

# Line chart with multiple lines 
st.line_chart(history.set_index("epoch"))

# Dataset statistics
st.header("Dataset Statistics")

# Sample dataset metrics
datasets = pd.DataFrame({
    "Dataset": ["Customer Data", "Sales Records", "Web Logs", "Sensor Data"],
    "Size (GB)": [12.5, 8.3, 45.2, 120.7],
    "Records": [50000, 120000, 1000000, 5000000],
    "Features": [25, 15, 10, 8]
})

st.dataframe(datasets, use_container_width=True)

# Bar chart for dataset sizes
st.subheader("Dataset Sizes Comparison")
st.bar_chart(datasets.set_index("Dataset")["Size (GB)"])

# Data quality metrics
st.header("Data Quality")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Completeness", "98.7%")

with col2:
    st.metric("Consistency", "96.2%")

with col3:
    st.metric("Accuracy", "94.8%")

("Sample correlation matrix")

# Navigation
st.markdown("---")
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

# AI Assistant Integration (Week 10)
st.markdown("---")  
if st.button(f"Ask  AI Assistant", use_container_width=True):
    st.switch_page("pages/6_AI_Assistant.py")

