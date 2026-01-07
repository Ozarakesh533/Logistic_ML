# ============================================================================
# FILE: mlProject/components/data_transformation.py
# ============================================================================
"""
Data Transformation Component.
"""
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from mlProject.entity.config_entity import DataTransformationConfig
from mlProject.utils.common import save_object
from mlProject.constants import CATEGORICAL_FEATURES, NUMERICAL_FEATURES, TARGET_CANCEL, TARGET_BROKEN_ROUTE
import logging

logging.basicConfig(level=logging.INFO)


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def engineer_features(self, df):
        """Feature engineering from booking_date."""
        if 'booking_date' in df.columns:
            df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce')
            df['year'] = df['booking_date'].dt.year
            df['month'] = df['booking_date'].dt.month
            df['day'] = df['booking_date'].dt.day
            df['day_of_week'] = df['booking_date'].dt.dayofweek
            df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        return df

    def initiate_data_transformation(self):
        """Transform data and create preprocessing pipeline."""
        logging.info("Starting data transformation...")
        
        # Load data
        train_df = pd.read_csv(self.config.train_data_path)
        test_df = pd.read_csv(self.config.test_data_path)
        
        # Feature engineering
        train_df = self.engineer_features(train_df)
        test_df = self.engineer_features(test_df)
        
        # Select features
        cat_features = [f for f in CATEGORICAL_FEATURES if f in train_df.columns]
        num_features = [f for f in NUMERICAL_FEATURES if f in train_df.columns]
        
        # Handle missing values
        for col in cat_features:
            train_df[col] = train_df[col].fillna('unknown')
            test_df[col] = test_df[col].fillna('unknown')
        
        for col in num_features:
            train_df[col] = train_df[col].fillna(train_df[col].median())
            test_df[col] = test_df[col].fillna(train_df[col].median())
        
        # Create preprocessing pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features),
                ('num', StandardScaler(), num_features)
            ]
        )
        
        # Fit and transform
        X_train = train_df[cat_features + num_features]
        X_test = test_df[cat_features + num_features]
        
        X_train_transformed = preprocessor.fit_transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)
        
        # Save preprocessor
        save_object(preprocessor, self.config.encoder_path)
        
        # Save transformed data
        np.save(os.path.join(self.config.root_dir, 'X_train.npy'), X_train_transformed)
        np.save(os.path.join(self.config.root_dir, 'X_test.npy'), X_test_transformed)
        np.save(os.path.join(self.config.root_dir, 'y_train_cancel.npy'), train_df[TARGET_CANCEL].values)
        np.save(os.path.join(self.config.root_dir, 'y_test_cancel.npy'), test_df[TARGET_CANCEL].values)
        np.save(os.path.join(self.config.root_dir, 'y_train_broken.npy'), train_df[TARGET_BROKEN_ROUTE].values)
        np.save(os.path.join(self.config.root_dir, 'y_test_broken.npy'), test_df[TARGET_BROKEN_ROUTE].values)
        
        logging.info(f"Transformed train shape: {X_train_transformed.shape}")
        logging.info(f"Transformed test shape: {X_test_transformed.shape}")
        logging.info("Data transformation completed.")
        
        return X_train_transformed, X_test_transformed


