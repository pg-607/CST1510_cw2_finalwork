
import bcrypt
import sqlite3
from pathlib import Path
import streamlit as st

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""  # CHANGED from "user_role" to "role"
    st.session_state.user_id = None
    st.success("Logged out successfully!")

def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def hash_password(password):
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def user_exists(username):
    """Check if username exists in database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def register_user(username, password, role="user"):
    """
    Register a new user in database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Basic validation
    if not username or not password:
        return False, "Username and password are required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        return False, error_msg
    
    # Check if user exists
    if user_exists(username):
        return False, "Username already exists"
    
    try:
        # Hash password
        password_hash = hash_password(password)
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        conn.close()
        
        return True, f"User '{username}' registered successfully"
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def authenticate_user(username, password):
    """
    Authenticate user against database.
    
    Returns:
        tuple: (success: bool, user_data: dict or None, message: str)
    """
    if not username or not password:
        return False, None, "Username and password are required"
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )
        user_row = cursor.fetchone()
        conn.close()
        
        if not user_row:
            return False, None, "User not found"
        
        if verify_password(password, user_row['password_hash']):
            user_data = {
                'id': user_row['id'],
                'username': user_row['username'],
                'role': user_row['role']  # This returns 'role' from database
            }
            return True, user_data, "Login successful"
        else:
            return False, None, "Incorrect password"
    except Exception as e:
        return False, None, f"Authentication error: {str(e)}"
    
def initialize_session_state():
   
    # Initialize authentication variables if they don't exist
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "username" not in st.session_state:
        st.session_state.username = ""
    
    if "role" not in st.session_state:  # CHANGED from "user_role" to "role"
        st.session_state.role = ""
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None