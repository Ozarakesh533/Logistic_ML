











# ============================================================================
# FILE: config.py (Alternative configuration approach)
# ============================================================================
"""
Configuration file for different environments.
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Paths
    DATA_DIR = 'data'
    ARTIFACTS_DIR = 'artifacts'
    
    # ML parameters
    TEST_SIZE = 0.2
    RANDOM_STATE = 42


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Add production-specific settings
    # e.g., database URLs, Redis cache, etc.


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}