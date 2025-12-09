"""User entity class for authentication."""

class User:
    """Represents a user in the Multi-Domain Intelligence Platform."""
    
    def __init__(self, user_id: int, username: str, password_hash: str, role: str):
        """
        Initialize a User instance.
        
        Args:
            user_id: Unique identifier for the user
            username: User's username
            password_hash: Hashed password
            role: User role (user, analyst, admin)
        """
        self.__id = user_id
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role
    
    def get_id(self) -> int:
        """Get user ID."""
        return self.__id
    
    def get_username(self) -> str:
        """Get username."""
        return self.__username
    
    def get_role(self) -> str:
        """Get user role."""
        return self.__role
    
    def get_password_hash(self) -> str:
        """Get password hash."""
        return self.__password_hash
    
    def verify_password(self, plain_password: str, hasher) -> bool:
        """
        Check if a plain-text password matches this user's hash.
        
        Args:
            plain_password: The password to verify
            hasher: Object with a check_password method
            
        Returns:
            bool: True if password matches
        """
        return hasher.check_password(plain_password, self.__password_hash)
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for session storage."""
        return {
            'id': self.__id,
            'username': self.__username,
            'role': self.__role
        }
    
    def __str__(self) -> str:
        """String representation of user."""
        return f"User({self.__username}, role={self.__role})"