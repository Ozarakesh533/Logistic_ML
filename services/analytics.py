# ============================================================================
# FILE: services/analytics.py
# ============================================================================
"""
Advanced analytics service for dashboard visualizations.
"""
import pandas as pd
import numpy as np
from database.database.models import query_scored_bookings
from datetime import datetime, timedelta


class AnalyticsService:
    """Service for computing advanced analytics."""
    
    def __init__(self):
        pass
    
    def get_dashboard_summary(self, filters=None):
        """Get summary statistics for dashboard."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return {
                'total_bookings': 0,
                'cancel_rate': 0,
                'broken_route_rate': 0,
                'high_risk_count': 0,
                'medium_risk_count': 0,
                'low_risk_count': 0,
                'avg_cancel_prob': 0,
                'avg_broken_prob': 0
            }
        
        # Compute statistics
        high_risk = len(df[df['cancel_risk'] == 'High'])
        medium_risk = len(df[df['cancel_risk'] == 'Medium'])
        low_risk = len(df[df['cancel_risk'] == 'Low'])
        
        # Count distinct booking_ids to avoid duplicates
        if 'booking_id' in df.columns:
            total_bookings = df['booking_id'].nunique()
        else:
            total_bookings = len(df)
        
        return {
            'total_bookings': total_bookings,
            'cancel_rate': df['cancel_probability'].mean() * 100,
            'broken_route_rate': df['broken_route_probability'].mean() * 100,
            'high_risk_count': high_risk,
            'medium_risk_count': medium_risk,
            'low_risk_count': low_risk,
            'avg_cancel_prob': df['cancel_probability'].mean() * 100,
            'avg_broken_prob': df['broken_route_probability'].mean() * 100
        }
    
    def get_bookings_over_time(self, filters=None, freq='D'):
        """Get bookings aggregated over time."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'booking_date' not in df.columns:
            return {'dates': [], 'counts': [], 'cancel_rates': []}
        
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        
        # Group by date
        grouped = df.groupby(df['booking_date'].dt.date).agg({
            'id': 'count',
            'cancel_probability': 'mean'
        }).reset_index()
        
        return {
            'dates': [str(d) for d in grouped['booking_date'].tolist()],
            'counts': grouped['id'].tolist(),
            'cancel_rates': [float(r * 100) for r in grouped['cancel_probability'].tolist()]
        }
    
    def get_cancellations_by_port(self, filters=None, top_n=10):
        """Get cancellation rates by port."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'pol' not in df.columns:
            return {'ports': [], 'cancel_rates': [], 'counts': []}
        
        grouped = df.groupby('pol').agg({
            'cancel_probability': 'mean',
            'id': 'count'
        }).reset_index()
        
        grouped = grouped.sort_values('cancel_probability', ascending=False).head(top_n)
        
        return {
            'ports': grouped['pol'].tolist(),
            'cancel_rates': [float(r * 100) for r in grouped['cancel_probability'].tolist()],
            'counts': grouped['id'].tolist()
        }
    
    def get_cancellations_by_lane(self, filters=None, top_n=10):
        """Get cancellation rates by lane."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'lane' not in df.columns:
            return {'lanes': [], 'cancel_rates': [], 'counts': []}
        
        grouped = df.groupby('lane').agg({
            'cancel_probability': 'mean',
            'id': 'count'
        }).reset_index()
        
        grouped = grouped.sort_values('cancel_probability', ascending=False).head(top_n)
        
        return {
            'lanes': grouped['lane'].tolist(),
            'cancel_rates': [float(r * 100) for r in grouped['cancel_probability'].tolist()],
            'counts': grouped['id'].tolist()
        }
    
    def get_risk_distribution(self, filters=None):
        """Get risk distribution."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'cancel_risk' not in df.columns:
            return {'labels': [], 'values': []}
        
        risk_counts = df['cancel_risk'].value_counts().to_dict()
        
        return {
            'labels': list(risk_counts.keys()),
            'values': list(risk_counts.values())
        }
    
    def get_flow_data(self, filters=None):
        """Get flow data for Sankey diagram."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return {'nodes': [], 'links': []}
        
        # Create flow: Lane -> Container State -> Risk
        flows = df.groupby(['lane', 'container_state', 'cancel_risk']).size().reset_index(name='value')
        
        # Create nodes (unique lanes, states, risks)
        lanes = sorted([str(l) for l in df['lane'].dropna().unique()])
        states = sorted([str(s) for s in df['container_state'].dropna().unique()])
        risks = ['Low', 'Medium', 'High']
        
        nodes = lanes + states + risks
        node_dict = {node: idx for idx, node in enumerate(nodes)}
        
        # Create links: Lane -> State -> Risk
        links = []
        for _, row in flows.iterrows():
            lane = str(row['lane'])
            state = str(row['container_state']) if pd.notna(row['container_state']) else None
            risk = str(row['cancel_risk']) if pd.notna(row['cancel_risk']) else None
            
            if lane in node_dict:
                # Link Lane -> State
                if state and state in node_dict:
                    links.append({
                        'source': node_dict[lane],
                        'target': node_dict[state],
                        'value': int(row['value'])
                    })
                # Link State -> Risk
                if state and state in node_dict and risk and risk in node_dict:
                    links.append({
                        'source': node_dict[state],
                        'target': node_dict[risk],
                        'value': int(row['value'])
                    })
        
        return {
            'nodes': [{'name': n} for n in nodes],
            'links': links
        }
    
    def get_seasonality_data(self, filters=None):
        """Get seasonality data for calendar heatmap."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'booking_date' not in df.columns:
            return {'dates': [], 'values': []}
        
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        
        # Group by date
        daily = df.groupby(df['booking_date'].dt.date).agg({
            'cancel_probability': 'mean'
        }).reset_index()
        
        return {
            'dates': [str(d) for d in daily['booking_date'].tolist()],
            'values': [float(v * 100) for v in daily['cancel_probability'].tolist()]
        }
    
    def get_network_data(self, filters=None):
        """Get network data for chord diagram (POL <-> POD)."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'pol' not in df.columns or 'pod' not in df.columns:
            return {'matrix': [], 'labels': []}
        
        # Get top ports
        top_pols = df['pol'].value_counts().head(10).index.tolist()
        top_pods = df['pod'].value_counts().head(10).index.tolist()
        ports = list(set(top_pols + top_pods))
        
        # Create matrix
        matrix = []
        for pol in ports:
            row = []
            for pod in ports:
                count = len(df[(df['pol'] == pol) & (df['pod'] == pod)])
                row.append(count)
            matrix.append(row)
        
        return {
            'matrix': matrix,
            'labels': ports
        }
    
    def get_top_risky_bookings(self, filters=None, top_n=10):
        """Get top risky bookings."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return []
        
        df_sorted = df.sort_values('cancel_probability', ascending=False).head(top_n)
        
        return df_sorted[[
            'booking_id', 'booking_date', 'pol', 'pod', 'lane',
            'cancel_probability', 'cancel_risk', 'broken_route_probability', 'broken_route_risk'
        ]].to_dict(orient='records')
    
    def get_risk_matrix_heatmap(self, filters=None):
        """Get risk matrix heatmap data (Port x Lane)."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'pol' not in df.columns or 'lane' not in df.columns:
            return {'ports': [], 'lanes': [], 'matrix': []}
        
        # Get top ports and lanes
        top_ports = df['pol'].value_counts().head(10).index.tolist()
        top_lanes = df['lane'].value_counts().head(10).index.tolist()
        
        # Create matrix
        matrix = []
        for port in top_ports:
            row = []
            for lane in top_lanes:
                subset = df[(df['pol'] == port) & (df['lane'] == lane)]
                if len(subset) > 0:
                    avg_prob = subset['cancel_probability'].mean() * 100
                else:
                    avg_prob = 0
                row.append(float(avg_prob))
            matrix.append(row)
        
        return {
            'ports': top_ports,
            'lanes': top_lanes,
            'matrix': matrix
        }
    
    def get_ridgeline_data(self, filters=None):
        """Get ridgeline plot data (volume over time per lane)."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'booking_date' not in df.columns or 'lane' not in df.columns:
            return {}
        
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        df['month'] = df['booking_date'].dt.to_period('M').astype(str)
        
        # Get top lanes
        top_lanes = df['lane'].value_counts().head(5).index.tolist()
        
        result = {}
        for lane in top_lanes:
            lane_df = df[df['lane'] == lane]
            monthly = lane_df.groupby('month').size()
            result[lane] = {
                'months': monthly.index.tolist(),
                'counts': monthly.values.tolist()
            }
        
        return result
    
    def get_stacked_area_data(self, filters=None):
        """Get stacked area chart data (bookings over time by lane)."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'booking_date' not in df.columns or 'lane' not in df.columns:
            return {'dates': [], 'lanes': [], 'data': []}
        
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        df['date'] = df['booking_date'].dt.date
        
        # Get top lanes
        top_lanes = df['lane'].value_counts().head(5).index.tolist()
        
        # Group by date and lane
        grouped = df.groupby(['date', 'lane']).size().reset_index(name='count')
        
        # Get all unique dates
        all_dates = sorted(df['date'].unique())
        
        # Build data structure
        data = []
        for lane in top_lanes:
            lane_data = []
            for date in all_dates:
                count = grouped[(grouped['date'] == date) & (grouped['lane'] == lane)]['count'].values
                lane_data.append(int(count[0]) if len(count) > 0 else 0)
            data.append(lane_data)
        
        return {
            'dates': [str(d) for d in all_dates],
            'lanes': top_lanes,
            'data': data
        }
    
    def get_waffle_data(self, filters=None):
        """Get waffle chart data (empty vs loaded vs cancelled vs idle)."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0:
            return {'labels': [], 'values': []}
        
        # Categorize by container_state and cancel_risk
        categories = {
            'Loaded': len(df[df['container_state'] == 'FCL']),
            'Empty': len(df[df['container_state'] == 'LCL']),
            'Cancelled': len(df[df['cancel_risk'] == 'High']),
            'Active': len(df[df['cancel_risk'] == 'Low'])
        }
        
        return {
            'labels': list(categories.keys()),
            'values': list(categories.values())
        }
    
    def get_top_risky_lanes(self, filters=None, top_n=5):
        """Get top risky lanes."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'lane' not in df.columns:
            return []
        
        grouped = df.groupby('lane').agg({
            'cancel_probability': 'mean',
            'id': 'count'
        }).reset_index()
        
        grouped = grouped.sort_values('cancel_probability', ascending=False).head(top_n)
        
        return grouped.to_dict(orient='records')
    
    def get_top_risky_ports(self, filters=None, top_n=5):
        """Get top risky ports."""
        df = query_scored_bookings(filters)
        
        if len(df) == 0 or 'pol' not in df.columns:
            return []
        
        grouped = df.groupby('pol').agg({
            'cancel_probability': 'mean',
            'id': 'count'
        }).reset_index()
        
        grouped = grouped.sort_values('cancel_probability', ascending=False).head(top_n)
        
        return grouped.to_dict(orient='records')