# ============================================================================
# FILE: mlProject/components/data_validation.py
# ============================================================================
"""
Data Validation Component.
"""
import pandas as pd
from mlProject.entity.config_entity import DataValidationConfig
from mlProject.utils.common import save_json
import logging

logging.basicConfig(level=logging.INFO)


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self):
        """Validate data quality and schema."""
        logging.info("Starting data validation...")
        
        df = pd.read_csv(self.config.data_path)
        
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'missing_columns': [],
            'missing_values': {},
            'data_types': {},
            'validation_status': 'PASSED'
        }
        
        # Check required columns
        for col in self.config.required_columns:
            if col not in df.columns:
                report['missing_columns'].append(col)
                report['validation_status'] = 'FAILED'
        
        # Missing values per column
        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            report['missing_values'][col] = f"{missing_pct:.2f}%"
            report['data_types'][col] = str(df[col].dtype)
        
        # Save report
        save_json(report, self.config.report_path)
        
        logging.info(f"Validation status: {report['validation_status']}")
        logging.info("Data validation completed.")
        
        return report


