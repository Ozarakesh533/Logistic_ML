# ============================================================================
# FILE: mlProject/pipeline/data_validation_pipeline.py
# ============================================================================
"""
Data validation pipeline.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_validation import DataValidation
import logging

logging.basicConfig(level=logging.INFO)


class DataValidationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        report = data_validation.validate_data()
        return report
