# ============================================================================
# FILE: mlProject/pipeline/data_transformation_pipeline.py
# ============================================================================
"""
Data transformation pipeline.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_transformation import DataTransformation
import logging

logging.basicConfig(level=logging.INFO)


class DataTransformationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        X_train, X_test = data_transformation.initiate_data_transformation()
        return X_train, X_test