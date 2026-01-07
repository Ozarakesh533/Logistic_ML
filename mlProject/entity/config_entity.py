# ============================================================================
# FILE: mlProject/entity/config_entity.py
# ============================================================================
"""
Configuration entities for each pipeline stage.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_path: Path
    train_path: Path
    test_path: Path
    test_size: float
    random_state: int


@dataclass
class DataValidationConfig:
    root_dir: Path
    data_path: Path
    required_columns: list
    report_path: Path


@dataclass
class DataTransformationConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    encoder_path: Path
    scaler_path: Path


@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    cancel_model_path: Path
    broken_route_model_path: Path


@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    cancel_model_path: Path
    broken_route_model_path: Path
    encoder_path: Path
    scaler_path: Path
    metrics_path: Path


