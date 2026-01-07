# ============================================================================
# FILE: mlProject/components/model_evaluation.py
# ============================================================================
"""
Model Evaluation Component.
"""
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from mlProject.entity.config_entity import ModelEvaluationConfig
from mlProject.utils.common import load_object, save_json
import logging
import os

logging.basicConfig(level=logging.INFO)


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate a single model."""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1': float(f1_score(y_test, y_pred, zero_division=0)),
            'auc': float(roc_auc_score(y_test, y_pred_proba)) if len(np.unique(y_test)) > 1 else 0.0
        }
        
        return metrics

    def initiate_model_evaluation(self):
        """Evaluate both models."""
        logging.info("Starting model evaluation...")
        
        # Load test data
        X_test = np.load(os.path.join(self.config.test_data_path, 'X_test.npy'))
        y_test_cancel = np.load(os.path.join(self.config.test_data_path, 'y_test_cancel.npy'))
        y_test_broken = np.load(os.path.join(self.config.test_data_path, 'y_test_broken.npy'))
        
        # Load models
        cancel_model = load_object(self.config.cancel_model_path)
        broken_model = load_object(self.config.broken_route_model_path)
        
        # Evaluate
        cancel_metrics = self.evaluate_model(cancel_model, X_test, y_test_cancel, "Cancel")
        broken_metrics = self.evaluate_model(broken_model, X_test, y_test_broken, "Broken Route")
        
        # Create metrics report
        metrics_report = {
            'cancel_model': {
                'best_model_name': type(cancel_model).__name__,
                'metrics': cancel_metrics
            },
            'broken_route_model': {
                'best_model_name': type(broken_model).__name__,
                'metrics': broken_metrics
            }
        }
        
        # Save
        save_json(metrics_report, self.config.metrics_path)
        
        logging.info("Model evaluation completed.")
        logging.info(f"Cancel Model - F1: {cancel_metrics['f1']:.4f}, AUC: {cancel_metrics['auc']:.4f}")
        logging.info(f"Broken Route Model - F1: {broken_metrics['f1']:.4f}, AUC: {broken_metrics['auc']:.4f}")
        
        return metrics_report