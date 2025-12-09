"""Security Incident Service for managing cybersecurity incidents."""

from typing import List, Optional
from models.security_incident import SecurityIncident
from services.database_manager import DatabaseManager


class IncidentService:
    """Service class for managing security incidents."""
    
    def __init__(self, db: DatabaseManager):
        """
        Initialize IncidentService.
        
        Args:
            db: DatabaseManager instance
        """
        self._db = db
    
    def get_all_incidents(self) -> List[SecurityIncident]:
        """
        Retrieve all security incidents.
        
        Returns:
            List[SecurityIncident]: List of all incidents
        """
        rows = self._db.fetch_all(
            """SELECT incident_id, timestamp, category, severity, status, description 
               FROM cyber_incidents ORDER BY incident_id DESC"""
        )
        
        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row['incident_id'],
                incident_type=row['category'],
                severity=row['severity'],
                status=row['status'],
                description=row['description'],
                timestamp=row['timestamp']
            )
            incidents.append(incident)
        
        return incidents
    
    def get_incident_by_id(self, incident_id: int) -> Optional[SecurityIncident]:
        """
        Get a specific incident by ID.
        
        Args:
            incident_id: ID of incident to retrieve
            
        Returns:
            Optional[SecurityIncident]: Incident object or None
        """
        row = self._db.fetch_one(
            """SELECT incident_id, timestamp, category, severity, status, description
               FROM cyber_incidents WHERE incident_id = ?""",
            (incident_id,)
        )
        
        if row:
            return SecurityIncident(
                incident_id=row['incident_id'],
                incident_type=row['category'],
                severity=row['severity'],
                status=row['status'],
                description=row['description'],
                timestamp=row['timestamp']
            )
        return None
    
    def get_incidents_by_severity(self, severity: str) -> List[SecurityIncident]:
        """
        Get incidents filtered by severity.
        
        Args:
            severity: Severity level to filter by
            
        Returns:
            List[SecurityIncident]: Filtered incidents
        """
        rows = self._db.fetch_all(
            """SELECT incident_id, timestamp, category, severity, status, description
               FROM cyber_incidents WHERE severity = ? ORDER BY incident_id DESC""",
            (severity,)
        )
        
        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row['incident_id'],
                incident_type=row['category'],
                severity=row['severity'],
                status=row['status'],
                description=row['description'],
                timestamp=row['timestamp']
            )
            incidents.append(incident)
        
        return incidents
    
    def get_incidents_by_status(self, status: str) -> List[SecurityIncident]:
        """
        Get incidents filtered by status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List[SecurityIncident]: Filtered incidents
        """
        rows = self._db.fetch_all(
            """SELECT incident_id, timestamp, category, severity, status, description
               FROM cyber_incidents WHERE status = ? ORDER BY incident_id DESC""",
            (status,)
        )
        
        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row['incident_id'],
                incident_type=row['category'],
                severity=row['severity'],
                status=row['status'],
                description=row['description'],
                timestamp=row['timestamp']
            )
            incidents.append(incident)
        
        return incidents
    
    def create_incident(self, incident_type: str, severity: str, 
                       description: str, reported_by: str = None) -> int:
        """
        Create a new security incident.
        
        Args:
            incident_type: Type/category of incident
            severity: Severity level
            description: Incident description
            reported_by: Who reported the incident
            
        Returns:
            int: ID of newly created incident
        """
        from datetime import datetime
        
        # Get next incident ID
        max_row = self._db.fetch_one(
            "SELECT MAX(incident_id) as max_id FROM cyber_incidents"
        )
        next_id = (max_row['max_id'] or 1000) + 1
        
        # Insert incident
        self._db.execute_query(
            """INSERT INTO cyber_incidents 
               (incident_id, timestamp, category, severity, status, description)
               VALUES (?, ?, ?, ?, 'Open', ?)""",
            (next_id, datetime.now().isoformat(), incident_type, severity, description)
        )
        
        return next_id
    
    def update_incident_status(self, incident_id: int, new_status: str) -> bool:
        """
        Update an incident's status.
        
        Args:
            incident_id: ID of incident to update
            new_status: New status value
            
        Returns:
            bool: True if update successful
        """
        cursor = self._db.execute_query(
            "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?",
            (new_status, incident_id)
        )
        return cursor.rowcount > 0
    
    def delete_incident(self, incident_id: int) -> bool:
        """
        Delete an incident.
        
        Args:
            incident_id: ID of incident to delete
            
        Returns:
            bool: True if deletion successful
        """
        cursor = self._db.execute_query(
            "DELETE FROM cyber_incidents WHERE incident_id = ?",
            (incident_id,)
        )
        return cursor.rowcount > 0
    
    def get_incident_count_by_category(self) -> dict:
        """
        Get count of incidents grouped by category.
        
        Returns:
            dict: Category counts
        """
        rows = self._db.fetch_all(
            """SELECT category, COUNT(*) as count 
               FROM cyber_incidents 
               GROUP BY category 
               ORDER BY count DESC"""
        )
        
        return {row['category']: row['count'] for row in rows}
    
    def get_high_severity_by_status(self) -> dict:
        """
        Get count of high severity incidents by status.
        
        Returns:
            dict: Status counts for high severity
        """
        rows = self._db.fetch_all(
            """SELECT status, COUNT(*) as count 
               FROM cyber_incidents 
               WHERE severity = 'High' 
               GROUP BY status 
               ORDER BY count DESC"""
        )
        
        return {row['status']: row['count'] for row in rows}