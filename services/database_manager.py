"""Database Manager service class."""

import sqlite3
from typing import Any, Iterable, Optional, List
from pathlib import Path


class DatabaseManager:
    """Handles SQLite database connections and queries."""
    
    def __init__(self, db_path: str):
        """
        Initialize DatabaseManager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self._db_path = Path(db_path)
        self._connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Establish database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(str(self._db_path))
            self._connection.row_factory = sqlite3.Row  # Enable column access by name
    
    def close(self) -> None:
        """Close database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def execute_query(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        """
        Execute a write query (INSERT, UPDATE, DELETE).
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            sqlite3.Cursor: Cursor object
        """
        if self._connection is None:
            self.connect()
        
        cursor = self._connection.cursor()
        cursor.execute(sql, tuple(params))
        self._connection.commit()
        return cursor
    
    def fetch_one(self, sql: str, params: Iterable[Any] = ()) -> Optional[sqlite3.Row]:
        """
        Fetch a single row.
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            Optional[sqlite3.Row]: Single row or None
        """
        if self._connection is None:
            self.connect()
        
        cursor = self._connection.cursor()
        cursor.execute(sql, tuple(params))
        return cursor.fetchone()
    
    def fetch_all(self, sql: str, params: Iterable[Any] = ()) -> List[sqlite3.Row]:
        """
        Fetch all rows.
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            List[sqlite3.Row]: List of rows
        """
        if self._connection is None:
            self.connect()
        
        cursor = self._connection.cursor()
        cursor.execute(sql, tuple(params))
        return cursor.fetchall()
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()