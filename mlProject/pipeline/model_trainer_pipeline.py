# ============================================================================
# FILE: mlProject/pipeline/model_trainer_pipeline.py
# ============================================================================
"""
Model training pipeline.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.model_trainer import ModelTrainer
import logging

logging.basicConfig(level=logging.INFO)


class ModelTrainerPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        results = model_trainer.initiate_model_training()
        return results
