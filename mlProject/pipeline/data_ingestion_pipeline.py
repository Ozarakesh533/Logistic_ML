# ============================================================================
# FILE: mlProject/pipeline/data_ingestion_pipeline.py
# ============================================================================
"""
Pipeline wrappers for easier execution.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_ingestion import DataIngestion
import logging

logging.basicConfig(level=logging.INFO)


class DataIngestionPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        train_path, test_path = data_ingestion.initiate_data_ingestion()
        return train_path, test_path