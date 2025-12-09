import streamlit as st
from datetime import datetime
# Page configuration
st.set_page_config(
    page_title="Settings",
    layout="wide"
)

# Initialize session state (defined locally to match other pages)
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
# Title
st.title("⚙️ Settings")

# User profile section
st.header("User Profile")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Username", value=st.session_state.username, disabled=True)
    st.text_input("Role", value=st.session_state.role, disabled=True)

with col2:
    # Password change
    with st.form("change_password"):
        st.subheader("Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Update Password"):
            if new_password == confirm_password:
                # Update password in session state (demo only)
                if st.session_state.username in st.session_state.users:
                    st.session_state.users[st.session_state.username] = new_password
                st.success("Password updated!")
            else:
                st.error("Passwords do not match")

# Platform settings
st.header("Platform Settings")

# Theme settings
theme = st.selectbox("Theme", ["Light", "Dark", "System"])
layout = st.selectbox("Layout", ["Wide", "Centered"])


# Save settings button
if st.button("Save Settings", type="primary"):
    st.success("Settings saved successfully!")

# Session information
st.header("Session Information")
st.write(f"Session ID: {id(st.session_state)}")
st.write(f"Logged in since: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Navigation
st.markdown("---")
if st.button("Back to Dashboard"):
    st.switch_page("pages/1_Dashboard.py")