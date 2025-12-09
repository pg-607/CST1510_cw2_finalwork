"""Dataset Service for managing data science datasets."""

from typing import List, Optional
from models.dataset import Dataset
from services.database_manager import DatabaseManager


class DatasetService:
    """Service class for managing datasets."""
    
    def __init__(self, db: DatabaseManager):
        """
        Initialize DatasetService.
        
        Args:
            db: DatabaseManager instance
        """
        self._db = db
    
    def get_all_datasets(self) -> List[Dataset]:
        """
        Retrieve all datasets.
        
        Returns:
            List[Dataset]: List of all datasets
        """
        rows = self._db.fetch_all(
            """SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
               FROM datasets_metadata ORDER BY dataset_id DESC"""
        )
        
        datasets = []
        for row in rows:
            dataset = Dataset(
                dataset_id=row['dataset_id'],
                name=row['name'],
                rows=row['rows'],
                columns=row['columns'],
                uploaded_by=row['uploaded_by'],
                upload_date=row['upload_date']
            )
            datasets.append(dataset)
        
        return datasets
    
    def get_dataset_by_id(self, dataset_id: int) -> Optional[Dataset]:
        """
        Get a specific dataset by ID.
        
        Args:
            dataset_id: ID of dataset to retrieve
            
        Returns:
            Optional[Dataset]: Dataset object or None
        """
        row = self._db.fetch_one(
            """SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
               FROM datasets_metadata WHERE dataset_id = ?""",
            (dataset_id,)
        )
        
        if row:
            return Dataset(
                dataset_id=row['dataset_id'],
                name=row['name'],
                rows=row['rows'],
                columns=row['columns'],
                uploaded_by=row['uploaded_by'],
                upload_date=row['upload_date']
            )
        return None
    
    def get_datasets_by_uploader(self, uploaded_by: str) -> List[Dataset]:
        """
        Get datasets filtered by uploader.
        
        Args:
            uploaded_by: Username of uploader
            
        Returns:
            List[Dataset]: Filtered datasets
        """
        rows = self._db.fetch_all(
            """SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
               FROM datasets_metadata WHERE uploaded_by = ? ORDER BY dataset_id DESC""",
            (uploaded_by,)
        )
        
        datasets = []
        for row in rows:
            dataset = Dataset(
                dataset_id=row['dataset_id'],
                name=row['name'],
                rows=row['rows'],
                columns=row['columns'],
                uploaded_by=row['uploaded_by'],
                upload_date=row['upload_date']
            )
            datasets.append(dataset)
        
        return datasets
    
    def create_dataset(self, name: str, rows: int, columns: int,
                      uploaded_by: str) -> int:
        """
        Create a new dataset record.
        
        Args:
            name: Dataset name
            rows: Number of rows
            columns: Number of columns
            uploaded_by: Who uploaded the dataset
            
        Returns:
            int: ID of newly created dataset
        """
        from datetime import datetime
        
        # Get next dataset ID
        max_row = self._db.fetch_one(
            "SELECT MAX(dataset_id) as max_id FROM datasets_metadata"
        )
        next_id = (max_row['max_id'] or 0) + 1
        
        upload_date = datetime.now().strftime('%Y-%m-%d')
        
        # Insert dataset
        self._db.execute_query(
            """INSERT INTO datasets_metadata 
               (dataset_id, name, rows, columns, uploaded_by, upload_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (next_id, name, rows, columns, uploaded_by, upload_date)
        )
        
        return next_id
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """
        Delete a dataset.
        
        Args:
            dataset_id: ID of dataset to delete
            
        Returns:
            bool: True if deletion successful
        """
        cursor = self._db.execute_query(
            "DELETE FROM datasets_metadata WHERE dataset_id = ?",
            (dataset_id,)
        )
        return cursor.rowcount > 0
    
    def get_total_records(self) -> int:
        """
        Get total number of records across all datasets.
        
        Returns:
            int: Total records
        """
        row = self._db.fetch_one(
            "SELECT SUM(rows) as total FROM datasets_metadata"
        )
        return row['total'] or 0
    
    def get_dataset_statistics(self) -> dict:
        """
        Get summary statistics for all datasets.
        
        Returns:
            dict: Statistics including count, total rows, avg columns
        """
        row = self._db.fetch_one(
            """SELECT 
                COUNT(*) as dataset_count,
                SUM(rows) as total_rows,
                AVG(columns) as avg_columns
               FROM datasets_metadata"""
        )
        
        return {
            'dataset_count': row['dataset_count'],
            'total_rows': row['total_rows'] or 0,
            'avg_columns': round(row['avg_columns'] or 0, 2)
        }