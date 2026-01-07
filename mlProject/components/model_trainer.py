# ============================================================================
# FILE: mlProject/components/model_trainer.py
# ============================================================================
"""
Model Trainer Component.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from mlProject.entity.config_entity import ModelTrainerConfig
from mlProject.utils.common import evaluate_models, save_object
import logging
import os

logging.basicConfig(level=logging.INFO)


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_training(self):
        """Train models for both targets."""
        logging.info("Starting model training...")
        
        # Load transformed data
        data_path = self.config.train_data_path
        X_train = np.load(os.path.join(data_path, 'X_train.npy'))
        X_test = np.load(os.path.join(data_path, 'X_test.npy'))
        y_train_cancel = np.load(os.path.join(data_path, 'y_train_cancel.npy'))
        y_test_cancel = np.load(os.path.join(data_path, 'y_test_cancel.npy'))
        y_train_broken = np.load(os.path.join(data_path, 'y_train_broken.npy'))
        y_test_broken = np.load(os.path.join(data_path, 'y_test_broken.npy'))
        
        # Define models
        models = {
            'LogisticRegression': LogisticRegression(max_iter=1000),
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'XGBoost': XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
        }
        
        # Train cancel model
        logging.info("\n=== Training CANCEL model ===")
        cancel_results, best_cancel_name, best_cancel_model = evaluate_models(
            X_train, y_train_cancel, X_test, y_test_cancel, models
        )
        save_object(best_cancel_model, self.config.cancel_model_path)
        logging.info(f"Best cancel model: {best_cancel_name}")
        
        # Train broken route model
        logging.info("\n=== Training BROKEN ROUTE model ===")
        broken_results, best_broken_name, best_broken_model = evaluate_models(
            X_train, y_train_broken, X_test, y_test_broken, models
        )
        save_object(best_broken_model, self.config.broken_route_model_path)
        logging.info(f"Best broken route model: {best_broken_name}")
        
        logging.info("Model training completed.")
        
        return {
            'cancel': {'name': best_cancel_name, 'results': cancel_results},
            'broken_route': {'name': best_broken_name, 'results': broken_results}
        }