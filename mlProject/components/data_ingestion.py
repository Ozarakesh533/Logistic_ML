# ============================================================================
# FILE: mlProject/components/data_ingestion.py
# ============================================================================
"""
Data Ingestion Component.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from mlProject.entity.config_entity import DataIngestionConfig
import logging

logging.basicConfig(level=logging.INFO)


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self):
        """Read data and split into train/test."""
        logging.info("Starting data ingestion...")
        
        # Read data
        df = pd.read_csv(self.config.source_path)
        logging.info(f"Loaded data with shape: {df.shape}")
        
        # Split
        train_df, test_df = train_test_split(
            df, 
            test_size=self.config.test_size, 
            random_state=self.config.random_state,
            stratify=df['cancel'] if 'cancel' in df.columns else None
        )
        
        # Save
        train_df.to_csv(self.config.train_path, index=False)
        test_df.to_csv(self.config.test_path, index=False)
        
        logging.info(f"Train set: {train_df.shape}, Test set: {test_df.shape}")
        logging.info("Data ingestion completed.")
        
        return self.config.train_path, self.config.test_path


