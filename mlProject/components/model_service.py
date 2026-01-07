# ============================================================================
# FILE: mlProject/components/model_service.py
# ============================================================================
"""
Model Service - Central service for loading models and making predictions.
"""
import pandas as pd
import numpy as np
from mlProject.utils.common import load_object, load_json
from mlProject.constants import *
import logging
import os

logging.basicConfig(level=logging.INFO)


class ModelService:
    def __init__(self):
        self.encoder = None
        self.cancel_model = None
        self.broken_route_model = None
        self.loaded = False
        
    def load_models(self):
        """Load all required models and transformers."""
        try:
            encoder_path = os.path.join(DATA_TRANSFORMATION_DIR, ENCODER_FILE)
            cancel_model_path = os.path.join(MODEL_TRAINER_DIR, CANCEL_MODEL_FILE)
            broken_route_model_path = os.path.join(MODEL_TRAINER_DIR, BROKEN_ROUTE_MODEL_FILE)
            
            self.encoder = load_object(encoder_path)
            self.cancel_model = load_object(cancel_model_path)
            self.broken_route_model = load_object(broken_route_model_path)
            
            self.loaded = True
            logging.info("All models loaded successfully!")
        except Exception as e:
            logging.error(f"Error loading models: {e}")
            raise
    
    def engineer_features(self, df):
        """Apply same feature engineering as training."""
        df = df.copy()
        if 'booking_date' in df.columns:
            df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce')
            df['year'] = df['booking_date'].dt.year
            df['month'] = df['booking_date'].dt.month
            df['day'] = df['booking_date'].dt.day
            df['day_of_week'] = df['booking_date'].dt.dayofweek
            df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        return df
    
    def preprocess(self, df):
        """Preprocess input data."""
        df = self.engineer_features(df)
        
        # Select features
        cat_features = [f for f in CATEGORICAL_FEATURES if f in df.columns]
        num_features = [f for f in NUMERICAL_FEATURES if f in df.columns]
        
        # Handle missing values
        for col in cat_features:
            if col in df.columns:
                df[col] = df[col].fillna('unknown')
        
        for col in num_features:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Select and transform
        X = df[cat_features + num_features]
        X_transformed = self.encoder.transform(X)
        
        return X_transformed
    
    def get_risk_label(self, probability):
        """Convert probability to risk label."""
        if probability < 0.33:
            return "Low"
        elif probability < 0.66:
            return "Medium"
        else:
            return "High"
    
    def predict_cancel(self, df):
        """Predict cancellation risk."""
        if not self.loaded:
            self.load_models()
        
        X = self.preprocess(df)
        proba = self.cancel_model.predict_proba(X)[:, 1]
        
        results = []
        for p in proba:
            results.append({
                'probability': float(p),
                'risk_label': self.get_risk_label(p)
            })
        return results
    
    def predict_broken_route(self, df):
        """Predict broken route risk."""
        if not self.loaded:
            self.load_models()
        
        X = self.preprocess(df)
        proba = self.broken_route_model.predict_proba(X)[:, 1]
        
        results = []
        for p in proba:
            results.append({
                'probability': float(p),
                'risk_label': self.get_risk_label(p)
            })
        return results
    
    def predict_all(self, df):
        """Predict both cancellation and broken route."""
        cancel_results = self.predict_cancel(df)
        broken_results = self.predict_broken_route(df)
        
        combined = []
        for i in range(len(cancel_results)):
            combined.append({
                'cancel': cancel_results[i],
                'broken_route': broken_results[i]
            })
        return combined


