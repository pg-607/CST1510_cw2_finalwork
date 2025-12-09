"""IT Ticket entity class for IT operations."""

class ITTicket:
    """Represents an IT support ticket."""
    
    def __init__(self, ticket_id: int, priority: str, description: str, 
                 status: str, assigned_to: str = None, created_at: str = None,
                 resolution_time_hours: int = None):
        """
        Initialize an ITTicket instance.
        
        Args:
            ticket_id: Unique identifier
            priority: Priority level (Low, Medium, High, Critical)
            description: Ticket description
            status: Current status (Open, In Progress, Resolved, Closed, Waiting for User)
            assigned_to: Who is assigned to the ticket
            created_at: When ticket was created
            resolution_time_hours: Time to resolve in hours
        """
        self.__id = ticket_id
        self.__priority = priority
        self.__description = description
        self.__status = status
        self.__assigned_to = assigned_to
        self.__created_at = created_at
        self.__resolution_time_hours = resolution_time_hours
    
    def get_id(self) -> int:
        """Get ticket ID."""
        return self.__id
    
    def get_priority(self) -> str:
        """Get priority level."""
        return self.__priority
    
    def get_description(self) -> str:
        """Get ticket description."""
        return self.__description
    
    def get_status(self) -> str:
        """Get current status."""
        return self.__status
    
    def get_assigned_to(self) -> str:
        """Get assignee."""
        return self.__assigned_to
    
    def get_created_at(self) -> str:
        """Get creation date."""
        return self.__created_at
    
    def get_resolution_time_hours(self) -> int:
        """Get resolution time in hours."""
        return self.__resolution_time_hours
    
    def assign_to(self, staff: str) -> None:
        """
        Assign ticket to a staff member.
        
        Args:
            staff: Staff member name
        """
        self.__assigned_to = staff
    
    def update_status(self, new_status: str) -> None:
        """
        Update ticket status.
        
        Args:
            new_status: New status value
        """
        self.__status = new_status
    
    def close_ticket(self) -> None:
        """Close the ticket."""
        self.__status = "Closed"
    
    def get_priority_level(self) -> int:
        """
        Get numeric priority level for sorting.
        
        Returns:
            int: Priority level (1=Low, 2=Medium, 3=High, 4=Critical)
        """
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__priority.lower(), 0)
    
    def to_dict(self) -> dict:
        """Convert ticket to dictionary."""
        return {
            'id': self.__id,
            'priority': self.__priority,
            'description': self.__description,
            'status': self.__status,
            'assigned_to': self.__assigned_to,
            'created_at': self.__created_at,
            'resolution_time_hours': self.__resolution_time_hours
        }
    
    def __str__(self) -> str:
        """String representation of ticket."""
        return (
            f"Ticket {self.__id}: {self.__description[:30]}... "
            f"[{self.__priority}] – {self.__status} "
            f"(assigned to: {self.__assigned_to or 'Unassigned'})"
        )