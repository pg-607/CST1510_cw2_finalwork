"""
Refactored Home.py - Login and Registration using OOP
"""
import streamlit as st
from pathlib import Path

# Import OOP services
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

# Initialize session state
def initialize_session_state():
    """Initialize session state variables."""
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

# Page configuration
st.set_page_config(
    page_title="Intelligence Platform - Login",
    page_icon="🔐",
    layout="centered"
)

# Initialize services (using OOP)
db = DatabaseManager(str(DB_PATH))
auth_manager = AuthManager(db)

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
            # Use AuthManager to login (returns User object or None)
            user = auth_manager.login_user(login_username, login_password)
            
            if user:
                # Store user information in session state
                st.session_state.logged_in = True
                st.session_state.username = user.get_username()
                st.session_state.role = user.get_role()
                st.session_state.user_id = user.get_id()
                
                st.success(f"✅ Welcome back, {login_username}!")
                
                # Add a small delay for better UX
                with st.spinner("Redirecting to dashboard..."):
                    import time
                    time.sleep(1)
                    st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("❌ Invalid username or password")
                
with tab_register:
    st.header("Create New Account")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
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
            # Use AuthManager to register user (all new users are 'user' role)
            success, message = auth_manager.register_user(new_username, new_password, "user")
            
            if success:
                st.success(f"✅ {message}")
                st.info("📋 Go to Login tab to sign in")
            else:
                st.error(f"❌ {message}")

# Close database connection when done
db.close()