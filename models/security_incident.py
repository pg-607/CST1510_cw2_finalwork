"""Security Incident entity class."""

class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""
    
    def __init__(self, incident_id: int, incident_type: str, severity: str, 
                 status: str, description: str, timestamp: str = None, 
                 reported_by: str = None):
        """
        Initialize a SecurityIncident instance.
        
        Args:
            incident_id: Unique identifier
            incident_type: Type/category of incident
            severity: Severity level (Low, Medium, High, Critical)
            status: Current status (Open, In Progress, Resolved, Closed)
            description: Incident description
            timestamp: When incident occurred
            reported_by: Who reported the incident
        """
        self.__id = incident_id
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description
        self.__timestamp = timestamp
        self.__reported_by = reported_by
    
    def get_id(self) -> int:
        """Get incident ID."""
        return self.__id
    
    def get_incident_type(self) -> str:
        """Get incident type."""
        return self.__incident_type
    
    def get_severity(self) -> str:
        """Get severity level."""
        return self.__severity
    
    def get_status(self) -> str:
        """Get current status."""
        return self.__status
    
    def get_description(self) -> str:
        """Get incident description."""
        return self.__description
    
    def get_timestamp(self) -> str:
        """Get incident timestamp."""
        return self.__timestamp
    
    def get_reported_by(self) -> str:
        """Get reporter."""
        return self.__reported_by
    
    def update_status(self, new_status: str) -> None:
        """
        Update the incident status.
        
        Args:
            new_status: New status value
        """
        self.__status = new_status
    
    def get_severity_level(self) -> int:
        """
        Return an integer severity level for sorting/filtering.
        
        Returns:
            int: Severity level (1=Low, 2=Medium, 3=High, 4=Critical)
        """
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)
    
    def to_dict(self) -> dict:
        """Convert incident to dictionary."""
        return {
            'id': self.__id,
            'incident_type': self.__incident_type,
            'severity': self.__severity,
            'status': self.__status,
            'description': self.__description,
            'timestamp': self.__timestamp,
            'reported_by': self.__reported_by
        }
    
    def __str__(self) -> str:
        """String representation of incident."""
        return f"Incident {self.__id} [{self.__severity.upper()}] {self.__incident_type} - {self.__status}"