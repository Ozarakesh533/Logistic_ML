# ============================================================================
# FILE: mlProject/pipeline/prediction_pipeline.py
# ============================================================================
"""
Prediction pipeline for batch processing.
"""
import pandas as pd
from mlProject.components.model_service import ModelService


class PredictionPipeline:
    def __init__(self):
        self.model_service = ModelService()
        self.model_service.load_models()
    
    def predict(self, data_path):
        """Run predictions on a CSV file."""
        df = pd.read_csv(data_path)
        predictions = self.model_service.predict_all(df)
        
        # Add to dataframe
        df['cancel_probability'] = [p['cancel']['probability'] for p in predictions]
        df['cancel_risk'] = [p['cancel']['risk_label'] for p in predictions]
        df['broken_route_probability'] = [p['broken_route']['probability'] for p in predictions]
        df['broken_route_risk'] = [p['broken_route']['risk_label'] for p in predictions]
        
        return df


