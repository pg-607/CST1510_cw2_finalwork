import streamlit as st
from app.auth import authenticate_user, register_user, initialize_session_state

# Initialize session
initialize_session_state()

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔐",
    layout="centered"
)

# Page header
st.title("🔐 Multi-Domain Intelligence Platform")
st.markdown("### Secure Access Portal")
st.markdown("---")

# Create tabs
tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

with tab_login:
    st.header("Login to Your Account")
    
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("🚀 Login", type="primary", use_container_width=True):
        if not login_username or not login_password:
            st.error("❌ Please enter both username and password")
        else:
            success, user_data, message = authenticate_user(login_username, login_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = user_data['username']
                st.session_state.role = user_data['role']  # CHANGED from "user_role" to "role"
                st.session_state.user_id = user_data['id']
                st.success(f"✅ Welcome back, {login_username}!")
                
                # Add a small delay for better UX
                with st.spinner("Redirecting to dashboard..."):
                    import time
                    time.sleep(1)
                    st.switch_page("pages/1_Dashboard.py")
            else:
                st.error(f"❌ {message}")
                
with tab_register:
    st.header("Create New Account")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    user_role = st.selectbox("Select role", ["user", "analyst", "admin"], key="register_role")
    
    # Password requirements display
    with st.expander("🔒 Password Requirements"):
        st.markdown("""
        Your password must have:
        - At least 8 characters
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)  
        - At least one number (0-9)
        """)
    
    if st.button("📋 Create Account", type="primary", use_container_width=True):
        # Basic validation
        if not new_username or not new_password:
            st.warning("⚠️ Please fill in all fields")
        elif len(new_username) < 3:
            st.error("❌ Username must be at least 3 characters")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match")
        else:
            # Register user
            success, message = register_user(new_username, new_password, user_role)
            if success:
                st.success(f"✅ {message}")
                st.info("📋 Go to Login tab to sign in")
            else:
                st.error(f"❌ {message}")


