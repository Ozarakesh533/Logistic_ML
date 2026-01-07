# ============================================================================
# FILE: backend/routes_pages.py
# ============================================================================
"""
Page routes - render HTML templates.
"""
from flask import Blueprint, render_template, redirect, url_for
from mlProject.utils.common import load_json
from mlProject.constants import MODEL_EVALUATION_DIR, METRICS_FILE
import os
import logging

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """Redirect to dashboard."""
    return redirect(url_for('pages.dashboard'))


@pages_bp.route('/dashboard')
def dashboard():
    """Dashboard page with overview and charts."""
    return render_template('dashboard.html')


@pages_bp.route('/predict')
def predict():
    """Single prediction page."""
    return render_template('predict.html')


@pages_bp.route('/bulk-predict')
def bulk_predict():
    """Bulk prediction page."""
    return render_template('bulk_predict.html')


@pages_bp.route('/models')
def models():
    """Model metrics page."""
    try:
        metrics_path = os.path.join(MODEL_EVALUATION_DIR, METRICS_FILE)
        metrics = load_json(metrics_path)
    except Exception as e:
        logging.error(f"Error loading metrics: {e}")
        metrics = None
    
    return render_template('models.html', metrics=metrics)


