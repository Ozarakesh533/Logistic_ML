# ============================================================================
# FILE: services/ingestion.py
# ============================================================================
"""
Unified data ingestion service.
Accepts CSV, Excel, JSON and standardizes column names.
"""
import pandas as pd
import os
from typing import Union
import logging

logging.basicConfig(level=logging.INFO)


class DataIngestionService:
    """Unified data ingestion service."""
    
    # Column mapping for standardization
    COLUMN_MAPPING = {
        'booking_no': 'booking_id',
        'booking_number': 'booking_id',
        'id': 'booking_id',
        'port_of_loading': 'pol',
        'origin': 'pol',
        'origin_port': 'pol',
        'port_of_discharge': 'pod',
        'destination': 'pod',
        'dest_port': 'pod',
        'destination_port': 'pod',
        'trade_lane': 'lane',
        'shipping_lane': 'lane',
        'container_type': 'container_state',
        'container': 'container_state',
        'package': 'bundle',
        'service_type': 'bundle',
        'date': 'booking_date',
        'created_date': 'booking_date',
    }
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json']
    
    def detect_file_type(self, file_path_or_obj) -> str:
        """Detect file type from extension or object."""
        if isinstance(file_path_or_obj, str):
            _, ext = os.path.splitext(file_path_or_obj)
            return ext.lower()
        else:
            # For file objects
            filename = getattr(file_path_or_obj, 'filename', '')
            _, ext = os.path.splitext(filename)
            return ext.lower()
    
    def read_file(self, file_path_or_obj) -> pd.DataFrame:
        """Read file and return DataFrame."""
        file_type = self.detect_file_type(file_path_or_obj)
        
        if file_type == '.csv':
            df = pd.read_csv(file_path_or_obj)
        elif file_type in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path_or_obj)
        elif file_type == '.json':
            df = pd.read_json(file_path_or_obj)
        else:
            raise ValueError(f"Unsupported file format: {file_type}")
        
        logging.info(f"Read {len(df)} records from {file_type} file")
        return df
    
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names."""
        df_std = df.copy()
        
        # Convert column names to lowercase for matching
        columns_lower = {col: col.lower() for col in df_std.columns}
        
        # Rename columns based on mapping
        rename_dict = {}
        for col, col_lower in columns_lower.items():
            if col_lower in self.COLUMN_MAPPING:
                rename_dict[col] = self.COLUMN_MAPPING[col_lower]
        
        df_std = df_std.rename(columns=rename_dict)
        
        # Handle duplicate columns (e.g., if both 'pod' and 'destination' exist)
        # Keep the first occurrence and drop duplicates
        df_std = df_std.loc[:, ~df_std.columns.duplicated()]
        
        # Ensure booking_date is datetime
        if 'booking_date' in df_std.columns:
            df_std['booking_date'] = pd.to_datetime(df_std['booking_date'], errors='coerce')
        
        # Ensure booking_id exists (use booking_no if available, otherwise create from index)
        if 'booking_id' not in df_std.columns:
            if 'booking_no' in df_std.columns:
                df_std['booking_id'] = df_std['booking_no']
            else:
                df_std['booking_id'] = df_std.index.astype(str)
        
        logging.info(f"Standardized columns: {list(df_std.columns)}")
        return df_std
    
    def ingest(self, file_path_or_obj) -> pd.DataFrame:
        """Main ingestion method."""
        # Read file
        df = self.read_file(file_path_or_obj)
        
        # Standardize columns
        df = self.standardize_columns(df)
        
        # Basic validation
        if len(df) == 0:
            raise ValueError("Empty dataset")
        
        return df
