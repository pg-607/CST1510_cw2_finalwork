"""
Refactored Data Science Page - Using OOP with Dataset and DatasetService
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Import OOP classes
from services.database_manager import DatabaseManager
from services.dataset_service import DatasetService

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Page configuration
st.set_page_config(
    page_title="Data Science Dashboard",
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
dataset_service = DatasetService(db)

# Title
st.title("📈 Data Science Dashboard")

# Get all datasets using the service
datasets = dataset_service.get_all_datasets()

# Get statistics
stats = dataset_service.get_dataset_statistics()

# Model performance metrics (placeholder)
st.header("Platform Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Datasets", stats['dataset_count'])

with col2:
    st.metric("Total Records", f"{stats['total_rows']:,}")

with col3:
    st.metric("Avg Columns", stats['avg_columns'])

# Display datasets
st.header("Available Datasets")

if datasets:
    # Convert dataset objects to DataFrame for display
    dataset_data = []
    for dataset in datasets:
        dataset_data.append({
            'ID': dataset.get_id(),
            'Name': dataset.get_name(),
            'Rows': f"{dataset.get_rows():,}",
            'Columns': dataset.get_columns(),
            'Uploaded By': dataset.get_uploaded_by(),
            'Upload Date': dataset.get_upload_date(),
            'Est. Size': dataset.calculate_size_estimate()
        })
    
    df = pd.DataFrame(dataset_data)
    st.dataframe(df, use_container_width=True)
    
    # Dataset sizes visualization
    st.subheader("Dataset Comparison")
    
    # Create chart data
    chart_data = pd.DataFrame({
        'Dataset': [d.get_name() for d in datasets],
        'Records': [d.get_rows() for d in datasets],
        'Uploader': [d.get_uploaded_by() for d in datasets]
    })

    # Chart selector
    st.subheader("Charts")
    chart_type = st.selectbox(
        "Select chart type",
        [
            "Dataset Sizes (Bar)",
            "Records by Dataset (Line)",
            "Datasets by Uploader (Pie)"
        ]
    )

    if chart_type == "Dataset Sizes (Bar)":
        st.bar_chart(chart_data.set_index('Dataset')['Records'])

    elif chart_type == "Records by Dataset (Line)":
        # Line chart of records per dataset
        st.line_chart(chart_data.set_index('Dataset')['Records'])

    else:  # Datasets by Uploader (Pie)
        uploaders = chart_data['Uploader'].fillna('Unknown')
        uploader_counts = uploaders.value_counts()
        if not uploader_counts.empty:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.pie(uploader_counts.values, labels=uploader_counts.index, autopct='%1.1f%%')
            ax.set_title('Datasets by Uploader')
            st.pyplot(fig)
        else:
            st.info('No uploader data available')
    
else:
    st.info("No datasets found")

# Dataset Management
st.header("Dataset Management")

# Display dataset details
if datasets:
    st.subheader("Dataset Details")
    
    # Select a dataset to view
    dataset_options = {
        f"{d.get_name()} (ID: {d.get_id()})": d
        for d in datasets
    }
    
    selected_key = st.selectbox("Select dataset", list(dataset_options.keys()))
    selected_dataset = dataset_options[selected_key]
    
    # Display details using object methods
    col1, col2 = st.columns(2)
    # Show dataset details
    with col1:
        st.write("**Dataset Information:**")
        st.write(f"- **ID:** {selected_dataset.get_id()}")
        st.write(f"- **Name:** {selected_dataset.get_name()}")
        st.write(f"- **Rows:** {selected_dataset.get_rows():,}")
        st.write(f"- **Columns:** {selected_dataset.get_columns()}")
    
    with col2:
        st.write("**Metadata:**")
        st.write(f"- **Uploaded By:** {selected_dataset.get_uploaded_by()}")
        st.write(f"- **Upload Date:** {selected_dataset.get_upload_date()}")
        st.write(f"- **Estimated Size:** {selected_dataset.calculate_size_estimate()}")
        st.write(f"- **String Repr:** {str(selected_dataset)}")

# Filter by uploader
st.subheader("Filter Datasets")

col1, col2 = st.columns(2)

with col1:
    # Get unique uploaders
    uploaders = list(set([d.get_uploaded_by() for d in datasets if d.get_uploaded_by()]))
    
    if uploaders:
        selected_uploader = st.selectbox("Filter by uploader", ["All"] + uploaders)
        
        if selected_uploader != "All":
            filtered_datasets = dataset_service.get_datasets_by_uploader(selected_uploader)
            st.write(f"**Datasets uploaded by {selected_uploader}:** {len(filtered_datasets)}")
            
            for dataset in filtered_datasets:
                st.write(f"- {dataset}")

# Data quality metrics (placeholder)
st.header("Data Quality Metrics")
col1, col2, col3 = st.columns(3)
 # Display placeholder metrics
with col1:
    st.metric("Completeness", "98.7%")

with col2:
    st.metric("Consistency", "96.2%")

with col3:
    st.metric("Accuracy", "94.8%")

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