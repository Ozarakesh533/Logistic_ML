# ============================================================================
# FILE: backend/routes_api.py
# ============================================================================
"""
API routes - JSON endpoints for frontend.
"""
from flask import Blueprint, request, jsonify, send_file
from backend import model_service
import pandas as pd
import numpy as np
from mlProject.constants import DATA_INGESTION_DIR
import os
import logging
import io

api_bp = Blueprint('api', __name__)


@api_bp.route('/stats/overview', methods=['GET'])
def get_overview_stats():
    """Get overview KPIs - now reads from bookings_scored."""
    try:
        from database.database.models import query_scored_bookings
        
        # Get filters from query params
        filters = {}
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        if request.args.get('lane'):
            filters['lane'] = request.args.get('lane')
        if request.args.get('pol'):
            filters['pol'] = request.args.get('pol')
        if request.args.get('month'):
            filters['month'] = request.args.get('month')
        if request.args.get('year'):
            filters['year'] = request.args.get('year')
        
        # Query from database
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return jsonify({
                'total_bookings': 0,
                'cancel_rate': 0,
                'broken_rate': 0,
                'unique_lanes': 0,
                'unique_ports': 0
            })
        
        # Count distinct booking_ids to avoid duplicates
        if 'booking_id' in df.columns:
            total_bookings = int(df['booking_id'].nunique())
        else:
            total_bookings = int(len(df))
        
        stats = {
            'total_bookings': total_bookings,
            'cancel_rate': float(df['cancel_probability'].mean() * 100) if 'cancel_probability' in df.columns else 0,
            'broken_rate': float(df['broken_route_probability'].mean() * 100) if 'broken_route_probability' in df.columns else 0,
            'unique_lanes': int(df['lane'].nunique()) if 'lane' in df.columns else 0,
            'unique_ports': int(df['pol'].nunique()) if 'pol' in df.columns else 0
        }
        
        return jsonify(stats)
    except Exception as e:
        logging.error(f"Error getting overview stats: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stats/charts', methods=['GET'])
def get_chart_data():
    """Get aggregated data for charts - now reads from bookings_scored."""
    try:
        from database.database.models import query_scored_bookings
        
        # Get filters from query params
        filters = {}
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        if request.args.get('lane'):
            filters['lane'] = request.args.get('lane')
        if request.args.get('pol'):
            filters['pol'] = request.args.get('pol')
        if request.args.get('month'):
            filters['month'] = request.args.get('month')
        if request.args.get('year'):
            filters['year'] = request.args.get('year')
        
        # Query from database
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return jsonify({
                'cancel_by_lane': {'labels': [], 'values': []},
                'cancel_by_port': {'labels': [], 'values': []},
                'bookings_over_time': {}
            })
        
        # Cancellations by lane
        cancel_by_lane = df.groupby('lane')['cancel_probability'].mean().sort_values(ascending=False).head(10)
        
        # Cancellations by port
        cancel_by_port = df.groupby('pol')['cancel_probability'].mean().sort_values(ascending=False).head(10)
        
        # Bookings over time (if booking_date exists)
        bookings_over_time = {}
        if 'booking_date' in df.columns:
            df['booking_date'] = pd.to_datetime(df['booking_date'], errors='coerce')
            df['month'] = df['booking_date'].dt.to_period('M').astype(str)
            bookings_over_time = df.groupby('month').size().to_dict()
        
        data = {
            'cancel_by_lane': {
                'labels': cancel_by_lane.index.tolist(),
                'values': [float(v) * 100 for v in cancel_by_lane.values]
            },
            'cancel_by_port': {
                'labels': cancel_by_port.index.tolist(),
                'values': [float(v) * 100 for v in cancel_by_port.values]
            },
            'bookings_over_time': bookings_over_time
        }
        
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting chart data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/predict', methods=['POST'])
def predict_single():
    """Predict for a single booking."""
    try:
        data = request.json
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Get predictions
        predictions = model_service.predict_all(df)
        
        return jsonify(predictions[0])
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/bulk-predict', methods=['POST'])
def predict_bulk():
    """Predict for bulk CSV upload."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Use unified ingestion service
        from services.ingestion import DataIngestionService
        from core.predictor import UnifiedPredictor
        from database.database.models import insert_scored_bookings
        
        ingestion_service = DataIngestionService()
        predictor = UnifiedPredictor()
        
        # Ingest and standardize
        df = ingestion_service.ingest(file)
        
        # Generate predictions
        df_enriched = predictor.predict_bookings(df)
        
        # Save to database
        insert_scored_bookings(df_enriched)
        logging.info(f"Saved {len(df_enriched)} scored bookings to database")
        
        # Convert to CSV
        output = io.StringIO()
        df_enriched.to_csv(output, index=False)
        output.seek(0)
        
        # Return preview and full data
        preview = df_enriched.head(10).to_dict(orient='records')
        
        return jsonify({
            'preview': preview,
            'total_records': len(df_enriched),
            'csv_data': output.getvalue()
        })
    except Exception as e:
        logging.error(f"Error in bulk prediction: {e}")
        return jsonify({'error': str(e)}), 500


def _get_filters_from_request():
    """Helper to extract filters from request."""
    filters = {}
    if request.args.get('start_date'):
        filters['start_date'] = request.args.get('start_date')
    if request.args.get('end_date'):
        filters['end_date'] = request.args.get('end_date')
    if request.args.get('lane'):
        filters['lane'] = request.args.get('lane')
    if request.args.get('pol'):
        filters['pol'] = request.args.get('pol')
    if request.args.get('pod'):
        filters['pod'] = request.args.get('pod')
    if request.args.get('month'):
        filters['month'] = request.args.get('month')
    if request.args.get('year'):
        filters['year'] = request.args.get('year')
    return filters


@api_bp.route('/dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    """Get dashboard summary with filters."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        summary = analytics.get_dashboard_summary(filters)
        return jsonify(summary)
    except Exception as e:
        logging.error(f"Error getting dashboard summary: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/bookings-over-time', methods=['GET'])
def get_bookings_over_time():
    """Get bookings over time data."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        freq = request.args.get('freq', 'D')
        data = analytics.get_bookings_over_time(filters, freq)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting bookings over time: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/cancellations-by-port', methods=['GET'])
def get_cancellations_by_port():
    """Get cancellations by port."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        top_n = int(request.args.get('top_n', 10))
        data = analytics.get_cancellations_by_port(filters, top_n)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting cancellations by port: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/cancellations-by-lane', methods=['GET'])
def get_cancellations_by_lane():
    """Get cancellations by lane."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        top_n = int(request.args.get('top_n', 10))
        data = analytics.get_cancellations_by_lane(filters, top_n)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting cancellations by lane: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk distribution."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_risk_distribution(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting risk distribution: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/flow-data', methods=['GET'])
def get_flow_data():
    """Get flow data for Sankey diagram."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_flow_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting flow data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/seasonality-data', methods=['GET'])
def get_seasonality_data():
    """Get seasonality data for calendar heatmap."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_seasonality_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting seasonality data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/network-data', methods=['GET'])
def get_network_data():
    """Get network data for chord diagram."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_network_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting network data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/filter-options', methods=['GET'])
def get_filter_options():
    """Get available filter options."""
    try:
        from database.database.models import get_filter_options
        options = get_filter_options()
        return jsonify(options)
    except Exception as e:
        logging.error(f"Error getting filter options: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/top-outliers', methods=['GET'])
def get_top_outliers():
    """Get top risky bookings."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        top_n = int(request.args.get('top_n', 10))
        data = analytics.get_top_risky_bookings(filters, top_n)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting top outliers: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/risk-matrix', methods=['GET'])
def get_risk_matrix():
    """Get risk matrix heatmap data."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_risk_matrix_heatmap(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting risk matrix: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/ridgeline-data', methods=['GET'])
def get_ridgeline_data():
    """Get ridgeline plot data."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_ridgeline_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting ridgeline data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stacked-area-data', methods=['GET'])
def get_stacked_area_data():
    """Get stacked area chart data."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_stacked_area_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting stacked area data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/waffle-data', methods=['GET'])
def get_waffle_data():
    """Get waffle chart data."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        data = analytics.get_waffle_data(filters)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting waffle data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/top-risky-lanes', methods=['GET'])
def get_top_risky_lanes():
    """Get top risky lanes."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        top_n = int(request.args.get('top_n', 5))
        data = analytics.get_top_risky_lanes(filters, top_n)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting top risky lanes: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/top-risky-ports', methods=['GET'])
def get_top_risky_ports():
    """Get top risky ports."""
    try:
        from services.analytics import AnalyticsService
        analytics = AnalyticsService()
        filters = _get_filters_from_request()
        top_n = int(request.args.get('top_n', 5))
        data = analytics.get_top_risky_ports(filters, top_n)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error getting top risky ports: {e}")
        return jsonify({'error': str(e)}), 500


