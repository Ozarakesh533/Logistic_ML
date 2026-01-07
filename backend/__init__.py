# ============================================================================
# FILE: backend/__init__.py
# ============================================================================
"""
Flask application factory.
"""
from flask import Flask
from mlProject.components.model_service import ModelService
import logging

# Initialize model service (singleton)
model_service = ModelService()

def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Load models on startup
    try:
        model_service.load_models()
        logging.info("Models loaded successfully!")
    except Exception as e:
        logging.warning(f"Could not load models on startup: {e}")
        logging.warning("Models will be loaded on first prediction request.")
    
    # Initialize database
    from database.database.models import init_database
    init_database()
    logging.info("Database initialized successfully!")
    
    # Register blueprints
    from backend.routes_pages import pages_bp
    from backend.routes_api import api_bp
    
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


