# ============================================================================
# FILE: train_model.py
# ============================================================================
"""
Training pipeline script - runs all ML pipelines.
"""
from mlProject.config.configuration import ConfigurationManager
from mlProject.components.data_ingestion import DataIngestion
from mlProject.components.data_validation import DataValidation
from mlProject.components.data_transformation import DataTransformation
from mlProject.components.model_trainer import ModelTrainer
from mlProject.components.model_evaluation import ModelEvaluation
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    """Run complete ML training pipeline."""
    
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Stage 1: Data Ingestion
    logging.info("\n" + "="*50)
    logging.info("STAGE 1: Data Ingestion")
    logging.info("="*50)
    data_ingestion_config = config_manager.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    train_path, test_path = data_ingestion.initiate_data_ingestion()
    
    # Stage 2: Data Validation
    logging.info("\n" + "="*50)
    logging.info("STAGE 2: Data Validation")
    logging.info("="*50)
    data_validation_config = config_manager.get_data_validation_config()
    data_validation = DataValidation(config=data_validation_config)
    validation_report = data_validation.validate_data()
    
    if validation_report['validation_status'] == 'FAILED':
        logging.error("Data validation failed! Check validation report.")
        return
    
    # Stage 3: Data Transformation
    logging.info("\n" + "="*50)
    logging.info("STAGE 3: Data Transformation")
    logging.info("="*50)
    data_transformation_config = config_manager.get_data_transformation_config()
    data_transformation = DataTransformation(config=data_transformation_config)
    X_train, X_test = data_transformation.initiate_data_transformation()
    
    # Stage 4: Model Training
    logging.info("\n" + "="*50)
    logging.info("STAGE 4: Model Training")
    logging.info("="*50)
    model_trainer_config = config_manager.get_model_trainer_config()
    model_trainer = ModelTrainer(config=model_trainer_config)
    training_results = model_trainer.initiate_model_training()
    
    # Stage 5: Model Evaluation
    logging.info("\n" + "="*50)
    logging.info("STAGE 5: Model Evaluation")
    logging.info("="*50)
    model_evaluation_config = config_manager.get_model_evaluation_config()
    model_evaluation = ModelEvaluation(config=model_evaluation_config)
    metrics_report = model_evaluation.initiate_model_evaluation()
    
    logging.info("\n" + "="*50)
    logging.info("Training Pipeline Completed Successfully!")
    logging.info("="*50)
    logging.info(f"Cancel Model: {metrics_report['cancel_model']['best_model_name']}")
    logging.info(f"  F1 Score: {metrics_report['cancel_model']['metrics']['f1']:.4f}")
    logging.info(f"  AUC: {metrics_report['cancel_model']['metrics']['auc']:.4f}")
    logging.info(f"Broken Route Model: {metrics_report['broken_route_model']['best_model_name']}")
    logging.info(f"  F1 Score: {metrics_report['broken_route_model']['metrics']['f1']:.4f}")
    logging.info(f"  AUC: {metrics_report['broken_route_model']['metrics']['auc']:.4f}")


if __name__ == '__main__':
    main()