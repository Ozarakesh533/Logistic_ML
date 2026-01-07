# ============================================================================
# FILE: mlProject/utils/common.py
# ============================================================================
"""
Common utility functions.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_val_score
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')


def save_object(obj, file_path):
    """Save object using joblib."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(obj, file_path)
    logging.info(f"Object saved to {file_path}")


def load_object(file_path):
    """Load object using joblib."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return joblib.load(file_path)


def save_json(data, file_path):
    """Save dictionary as JSON."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"JSON saved to {file_path}")


def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def evaluate_models(X_train, y_train, X_test, y_test, models, params=None):
    """
    Train multiple models and evaluate them.
    Returns dict of model_name: metrics and the best model.
    """
    results = {}
    
    for model_name, model in models.items():
        logging.info(f"Training {model_name}...")
        
        # Apply hyperparameters if provided
        if params and model_name in params:
            model.set_params(**params[model_name])
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
        
        # Metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'auc': roc_auc_score(y_test, y_pred_proba) if len(np.unique(y_test)) > 1 else 0.0
        }
        
        results[model_name] = {
            'model': model,
            'metrics': metrics
        }
        
        logging.info(f"{model_name} - F1: {metrics['f1']:.4f}, AUC: {metrics['auc']:.4f}, Recall: {metrics['recall']:.4f}")
    
    # Select best model (prioritize F1 and AUC with good recall)
    best_model_name = max(results.keys(), 
                          key=lambda x: results[x]['metrics']['f1'] + results[x]['metrics']['auc'])
    
    return results, best_model_name, results[best_model_name]['model']


