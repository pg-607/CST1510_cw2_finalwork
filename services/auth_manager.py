"""Authentication Manager service class."""

import bcrypt
from typing import Optional, Tuple
from models.user import User
from services.database_manager import DatabaseManager


class PasswordHasher:
    """Handles password hashing and verification using bcrypt."""
    
    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hash a plain text password.
        
        Args:
            plain_password: Password to hash
            
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to check against
            
        Returns:
            bool: True if password matches
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False


class AuthManager:
    """Handles user registration and authentication."""
    
    def __init__(self, db: DatabaseManager):
        """
        Initialize AuthManager.
        
        Args:
            db: DatabaseManager instance for database operations
        """
        self._db = db
        self._hasher = PasswordHasher()
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
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
    
    def user_exists(self, username: str) -> bool:
        """
        Check if a username already exists.
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if user exists
        """
        row = self._db.fetch_one(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        return row is not None
    
    def register_user(self, username: str, password: str, role: str = "user") -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Username for new user
            password: Plain text password
            role: User role (default: "user")
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        # Validate password
        is_valid, error_msg = self.validate_password(password)
        if not is_valid:
            return False, error_msg
        
        # Check if user exists
        if self.user_exists(username):
            return False, "Username already exists"
        
        try:
            # Hash password
            password_hash = self._hasher.hash_password(password)
            
            # Insert into database
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            
            return True, f"User '{username}' registered successfully"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user and return User object if successful.
        
        Args:
            username: Username to authenticate
            password: Plain text password
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        if not username or not password:
            return None
        
        try:
            # Fetch user from database
            row = self._db.fetch_one(
                "SELECT id, username, password_hash, role FROM users WHERE username = ?",
                (username,)
            )
            
            if row is None:
                return None
            
            # Create User object and verify password
            user = User(
                user_id=row['id'],
                username=row['username'],
                password_hash=row['password_hash'],
                role=row['role']
            )
            
            # Verify password using the User object's method
            if user.verify_password(password, self._hasher):
                return user
            else:
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None