# ============================================================================
# FILE: mlProject/constants/__init__.py
# ============================================================================
"""
Central constants for the ML project.
Easy to modify when switching to real company data.
"""
import os
from pathlib import Path

# Root paths
ROOT_DIR = Path(__file__).parent.parent.parent
ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")

# Artifact subdirectories
DATA_INGESTION_DIR = os.path.join(ARTIFACTS_DIR, "data_ingestion")
DATA_VALIDATION_DIR = os.path.join(ARTIFACTS_DIR, "data_validation")
DATA_TRANSFORMATION_DIR = os.path.join(ARTIFACTS_DIR, "data_transformation")
MODEL_TRAINER_DIR = os.path.join(ARTIFACTS_DIR, "model_trainer")
MODEL_EVALUATION_DIR = os.path.join(ARTIFACTS_DIR, "model_evaluation")

# Data paths (configure for your dataset)
DATA_PATH = os.path.join(ROOT_DIR, "data", "logistics_data.csv")

# Column name mapping (ADJUST THIS for real data)
COLUMN_MAPPING = {
    "booking_no": "booking_no",
    "pol": "pol",
    "pod": "pod",
    "destination": "destination",
    "lane": "lane",
    "container_state": "container_state",
    "bundle": "bundle",
    "cancel": "cancel",
    "broken_route": "broken_route",
    "booking_date": "booking_date",
    "origin_id": "origin_id",
    "destination_id": "destination_id"
}

# Required columns for training
REQUIRED_COLUMNS = ["pol", "lane", "container_state", "cancel", "broken_route"]

# Target columns
TARGET_CANCEL = "cancel"
TARGET_BROKEN_ROUTE = "broken_route"

# Feature columns (categorical + numerical)
CATEGORICAL_FEATURES = ["pol", "pod", "lane", "container_state", "bundle"]
NUMERICAL_FEATURES = ["year", "month", "day", "day_of_week"]

# Training parameters
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model file names
CANCEL_MODEL_FILE = "cancel_model.pkl"
BROKEN_ROUTE_MODEL_FILE = "broken_route_model.pkl"
ENCODER_FILE = "encoder.pkl"
SCALER_FILE = "scaler.pkl"
METRICS_FILE = "metrics.json"


