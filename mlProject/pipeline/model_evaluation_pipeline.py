# ============================================================================
# FILE: mlProject/pipeline/model_evaluation_pipeline.py
# ============================================================================
"""
Model evaluation pipeline.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.model_evaluation import ModelEvaluation
import logging

logging.basicConfig(level=logging.INFO)


class ModelEvaluationPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        metrics = model_evaluation.initiate_model_evaluation()
        return metrics
