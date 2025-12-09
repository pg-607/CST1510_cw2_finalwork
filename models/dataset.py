"""Dataset entity class for data science operations."""

class Dataset:
    """Represents a data science dataset in the platform."""
    
    def __init__(self, dataset_id: int, name: str, rows: int, columns: int,
                 uploaded_by: str = None, upload_date: str = None):
        """
        Initialize a Dataset instance.
        
        Args:
            dataset_id: Unique identifier
            name: Dataset name
            rows: Number of rows
            columns: Number of columns
            uploaded_by: Who uploaded the dataset
            upload_date: When dataset was uploaded
        """
        self.__id = dataset_id
        self.__name = name
        self.__rows = rows
        self.__columns = columns
        self.__uploaded_by = uploaded_by
        self.__upload_date = upload_date
    
    def get_id(self) -> int:
        """Get dataset ID."""
        return self.__id
    
    def get_name(self) -> str:
        """Get dataset name."""
        return self.__name
    
    def get_rows(self) -> int:
        """Get number of rows."""
        return self.__rows
    
    def get_columns(self) -> int:
        """Get number of columns."""
        return self.__columns
    
    def get_uploaded_by(self) -> str:
        """Get uploader."""
        return self.__uploaded_by
    
    def get_upload_date(self) -> str:
        """Get upload date."""
        return self.__upload_date
    
    def calculate_size_estimate(self) -> str:
        """
        Estimate dataset size based on rows and columns.
        
        Returns:
            str: Human-readable size estimate
        """
        # Rough estimate: assume 100 bytes per cell
        size_bytes = self.__rows * self.__columns * 100
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb < 1:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_mb < 1024:
            return f"{size_mb:.2f} MB"
        else:
            return f"{size_mb / 1024:.2f} GB"
    
    def to_dict(self) -> dict:
        """Convert dataset to dictionary."""
        return {
            'id': self.__id,
            'name': self.__name,
            'rows': self.__rows,
            'columns': self.__columns,
            'uploaded_by': self.__uploaded_by,
            'upload_date': self.__upload_date
        }
    
    def __str__(self) -> str:
        """String representation of dataset."""
        return f"Dataset {self.__id}: {self.__name} ({self.__rows} rows, {self.__columns} cols)"