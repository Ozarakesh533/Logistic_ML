# ============================================================================
# FILE: mlProject/config/configuration.py
# ============================================================================
"""
Configuration manager to create config entities.
"""
import os
from pathlib import Path
from mlProject.constants import *
from mlProject.entity.config_entity import *


class ConfigurationManager:
    def __init__(self):
        # Create artifact directories
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        os.makedirs(DATA_INGESTION_DIR, exist_ok=True)
        os.makedirs(DATA_VALIDATION_DIR, exist_ok=True)
        os.makedirs(DATA_TRANSFORMATION_DIR, exist_ok=True)
        os.makedirs(MODEL_TRAINER_DIR, exist_ok=True)
        os.makedirs(MODEL_EVALUATION_DIR, exist_ok=True)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        return DataIngestionConfig(
            root_dir=Path(DATA_INGESTION_DIR),
            source_path=Path(DATA_PATH),
            train_path=Path(os.path.join(DATA_INGESTION_DIR, "train.csv")),
            test_path=Path(os.path.join(DATA_INGESTION_DIR, "test.csv")),
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE
        )

    def get_data_validation_config(self) -> DataValidationConfig:
        return DataValidationConfig(
            root_dir=Path(DATA_VALIDATION_DIR),
            data_path=Path(os.path.join(DATA_INGESTION_DIR, "train.csv")),
            required_columns=REQUIRED_COLUMNS,
            report_path=Path(os.path.join(DATA_VALIDATION_DIR, "validation_report.json"))
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        return DataTransformationConfig(
            root_dir=Path(DATA_TRANSFORMATION_DIR),
            train_data_path=Path(os.path.join(DATA_INGESTION_DIR, "train.csv")),
            test_data_path=Path(os.path.join(DATA_INGESTION_DIR, "test.csv")),
            encoder_path=Path(os.path.join(DATA_TRANSFORMATION_DIR, ENCODER_FILE)),
            scaler_path=Path(os.path.join(DATA_TRANSFORMATION_DIR, SCALER_FILE))
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        return ModelTrainerConfig(
            root_dir=Path(MODEL_TRAINER_DIR),
            train_data_path=Path(DATA_TRANSFORMATION_DIR),
            cancel_model_path=Path(os.path.join(MODEL_TRAINER_DIR, CANCEL_MODEL_FILE)),
            broken_route_model_path=Path(os.path.join(MODEL_TRAINER_DIR, BROKEN_ROUTE_MODEL_FILE))
        )

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        return ModelEvaluationConfig(
            root_dir=Path(MODEL_EVALUATION_DIR),
            test_data_path=Path(DATA_TRANSFORMATION_DIR),
            cancel_model_path=Path(os.path.join(MODEL_TRAINER_DIR, CANCEL_MODEL_FILE)),
            broken_route_model_path=Path(os.path.join(MODEL_TRAINER_DIR, BROKEN_ROUTE_MODEL_FILE)),
            encoder_path=Path(os.path.join(DATA_TRANSFORMATION_DIR, ENCODER_FILE)),
            scaler_path=Path(os.path.join(DATA_TRANSFORMATION_DIR, SCALER_FILE)),
            metrics_path=Path(os.path.join(MODEL_EVALUATION_DIR, METRICS_FILE))
        )


