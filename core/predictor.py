# ============================================================================
# FILE: core/predictor.py
# ============================================================================
"""
Unified ML predictor.
Loads existing models and generates predictions.
"""
import pandas as pd
import numpy as np
from mlProject.components.model_service import ModelService
import logging

logging.basicConfig(level=logging.INFO)


class UnifiedPredictor:
    """Unified prediction service."""
    
    def __init__(self):
        self.model_service = ModelService()
        self.loaded = False
    
    def load_models(self):
        """Load ML models."""
        if not self.loaded:
            self.model_service.load_models()
            self.loaded = True
            logging.info("Models loaded successfully")
    
    def compute_risk_bucket(self, probability: float) -> str:
        """Compute risk bucket from probability."""
        if probability < 0.33:
            return "Low"
        elif probability < 0.66:
            return "Medium"
        else:
            return "High"
    
    def predict_bookings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main prediction method.
        
        Args:
            df: DataFrame with booking data
        
        Returns:
            DataFrame enriched with predictions
        """
        if not self.loaded:
            self.load_models()
        
        df_result = df.copy()
        
        # Get predictions
        predictions = self.model_service.predict_all(df)
        
        # Add predictions to dataframe
        df_result['cancel_probability'] = [p['cancel']['probability'] for p in predictions]
        df_result['cancel_risk'] = [p['cancel']['risk_label'] for p in predictions]
        df_result['broken_route_probability'] = [p['broken_route']['probability'] for p in predictions]
        df_result['broken_route_risk'] = [p['broken_route']['risk_label'] for p in predictions]
        
        logging.info(f"Generated predictions for {len(df_result)} bookings")
        
        return df_result
