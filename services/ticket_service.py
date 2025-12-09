"""IT Ticket Service for managing IT operations tickets."""

from typing import List, Optional
from models.it_ticket import ITTicket
from services.database_manager import DatabaseManager


class TicketService:
    """Service class for managing IT tickets."""
    
    def __init__(self, db: DatabaseManager):
        """
        Initialize TicketService.
        
        Args:
            db: DatabaseManager instance
        """
        self._db = db
    
    def get_all_tickets(self) -> List[ITTicket]:
        """
        Retrieve all IT tickets.
        
        Returns:
            List[ITTicket]: List of all tickets
        """
        rows = self._db.fetch_all(
            """SELECT ticket_id, priority, description, status, 
                      assigned_to, created_at, resolution_time_hours
               FROM it_tickets ORDER BY ticket_id DESC"""
        )
        
        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row['ticket_id'],
                priority=row['priority'],
                description=row['description'],
                status=row['status'],
                assigned_to=row['assigned_to'],
                created_at=row['created_at'],
                resolution_time_hours=row['resolution_time_hours']
            )
            tickets.append(ticket)
        
        return tickets
    
    def get_ticket_by_id(self, ticket_id: int) -> Optional[ITTicket]:
        """
        Get a specific ticket by ID.
        
        Args:
            ticket_id: ID of ticket to retrieve
            
        Returns:
            Optional[ITTicket]: Ticket object or None
        """
        row = self._db.fetch_one(
            """SELECT ticket_id, priority, description, status,
                      assigned_to, created_at, resolution_time_hours
               FROM it_tickets WHERE ticket_id = ?""",
            (ticket_id,)
        )
        
        if row:
            return ITTicket(
                ticket_id=row['ticket_id'],
                priority=row['priority'],
                description=row['description'],
                status=row['status'],
                assigned_to=row['assigned_to'],
                created_at=row['created_at'],
                resolution_time_hours=row['resolution_time_hours']
            )
        return None
    
    def get_tickets_by_status(self, status: str) -> List[ITTicket]:
        """
        Get tickets filtered by status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List[ITTicket]: Filtered tickets
        """
        rows = self._db.fetch_all(
            """SELECT ticket_id, priority, description, status,
                      assigned_to, created_at, resolution_time_hours
               FROM it_tickets WHERE status = ? ORDER BY ticket_id DESC""",
            (status,)
        )
        
        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row['ticket_id'],
                priority=row['priority'],
                description=row['description'],
                status=row['status'],
                assigned_to=row['assigned_to'],
                created_at=row['created_at'],
                resolution_time_hours=row['resolution_time_hours']
            )
            tickets.append(ticket)
        
        return tickets
    
    def get_tickets_by_priority(self, priority: str) -> List[ITTicket]:
        """
        Get tickets filtered by priority.
        
        Args:
            priority: Priority level to filter by
            
        Returns:
            List[ITTicket]: Filtered tickets
        """
        rows = self._db.fetch_all(
            """SELECT ticket_id, priority, description, status,
                      assigned_to, created_at, resolution_time_hours
               FROM it_tickets WHERE priority = ? ORDER BY ticket_id DESC""",
            (priority,)
        )
        
        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row['ticket_id'],
                priority=row['priority'],
                description=row['description'],
                status=row['status'],
                assigned_to=row['assigned_to'],
                created_at=row['created_at'],
                resolution_time_hours=row['resolution_time_hours']
            )
            tickets.append(ticket)
        
        return tickets
    
    def get_tickets_by_assignee(self, assigned_to: str) -> List[ITTicket]:
        """
        Get tickets assigned to a specific person.
        
        Args:
            assigned_to: Assignee name
            
        Returns:
            List[ITTicket]: Filtered tickets
        """
        rows = self._db.fetch_all(
            """SELECT ticket_id, priority, description, status,
                      assigned_to, created_at, resolution_time_hours
               FROM it_tickets WHERE assigned_to = ? ORDER BY ticket_id DESC""",
            (assigned_to,)
        )
        
        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row['ticket_id'],
                priority=row['priority'],
                description=row['description'],
                status=row['status'],
                assigned_to=row['assigned_to'],
                created_at=row['created_at'],
                resolution_time_hours=row['resolution_time_hours']
            )
            tickets.append(ticket)
        
        return tickets
    
    def create_ticket(self, priority: str, description: str,
                     assigned_to: str = None) -> int:
        """
        Create a new IT ticket.
        
        Args:
            priority: Priority level
            description: Ticket description
            assigned_to: Who to assign the ticket to
            
        Returns:
            int: ID of newly created ticket
        """
        from datetime import datetime
        
        # Get next ticket ID
        max_row = self._db.fetch_one(
            "SELECT MAX(ticket_id) as max_id FROM it_tickets"
        )
        next_id = (max_row['max_id'] or 2000) + 1
        
        created_at = datetime.now().isoformat()
        
        # Insert ticket
        self._db.execute_query(
            """INSERT INTO it_tickets 
               (ticket_id, priority, description, status, assigned_to, created_at)
               VALUES (?, ?, ?, 'Open', ?, ?)""",
            (next_id, priority, description, assigned_to, created_at)
        )
        
        return next_id
    
    def update_ticket_status(self, ticket_id: int, new_status: str) -> bool:
        """
        Update a ticket's status.
        
        Args:
            ticket_id: ID of ticket to update
            new_status: New status value
            
        Returns:
            bool: True if update successful
        """
        cursor = self._db.execute_query(
            "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
            (new_status, ticket_id)
        )
        return cursor.rowcount > 0
    
    def assign_ticket(self, ticket_id: int, assigned_to: str) -> bool:
        """
        Assign a ticket to someone.
        
        Args:
            ticket_id: ID of ticket to assign
            assigned_to: Person to assign to
            
        Returns:
            bool: True if assignment successful
        """
        cursor = self._db.execute_query(
            "UPDATE it_tickets SET assigned_to = ? WHERE ticket_id = ?",
            (assigned_to, ticket_id)
        )
        return cursor.rowcount > 0
    
    def delete_ticket(self, ticket_id: int) -> bool:
        """
        Delete a ticket.
        
        Args:
            ticket_id: ID of ticket to delete
            
        Returns:
            bool: True if deletion successful
        """
        cursor = self._db.execute_query(
            "DELETE FROM it_tickets WHERE ticket_id = ?",
            (ticket_id,)
        )
        return cursor.rowcount > 0
    
    def get_ticket_statistics(self) -> dict:
        """
        Get summary statistics for tickets.
        
        Returns:
            dict: Statistics including counts by status and priority
        """
        # Count by status
        status_rows = self._db.fetch_all(
            """SELECT status, COUNT(*) as count 
               FROM it_tickets 
               GROUP BY status"""
        )
        
        # Count by priority
        priority_rows = self._db.fetch_all(
            """SELECT priority, COUNT(*) as count 
               FROM it_tickets 
               GROUP BY priority"""
        )
        
        # Average resolution time
        avg_row = self._db.fetch_one(
            """SELECT AVG(resolution_time_hours) as avg_time 
               FROM it_tickets 
               WHERE resolution_time_hours IS NOT NULL"""
        )
        
        return {
            'by_status': {row['status']: row['count'] for row in status_rows},
            'by_priority': {row['priority']: row['count'] for row in priority_rows},
            'avg_resolution_hours': round(avg_row['avg_time'] or 0, 2)
        }