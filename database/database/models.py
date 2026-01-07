# ============================================================================
# FILE: database/models.py
# ============================================================================
"""
Database models for persistent storage.
Uses SQLite for simplicity, easily upgradable to PostgreSQL.
"""
from datetime import datetime
import sqlite3
import pandas as pd
import os
from mlProject.constants import ARTIFACTS_DIR

DATABASE_PATH = os.path.join(ARTIFACTS_DIR, 'logistics.db')


def init_database():
    """Initialize database and create tables."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create bookings_scored table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings_scored (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT,
            booking_date DATE,
            pol TEXT,
            pod TEXT,
            lane TEXT,
            bundle TEXT,
            container_state TEXT,
            cancel_probability REAL,
            cancel_risk TEXT,
            broken_route_probability REAL,
            broken_route_risk TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_booking_date ON bookings_scored(booking_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_lane ON bookings_scored(lane)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pol ON bookings_scored(pol)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pod ON bookings_scored(pod)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON bookings_scored(created_at)')
    
    conn.commit()
    conn.close()


def insert_scored_bookings(df, replace_duplicates=False):
    """
    Insert scored bookings into database.
    
    Args:
        df: DataFrame with booking data
        replace_duplicates: If True, replace existing records with same booking_id
    """
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Prepare dataframe
    df_insert = df.copy()
    df_insert['created_at'] = datetime.now()
    
    # Select only required columns
    columns = [
        'booking_id', 'booking_date', 'pol', 'pod', 'lane', 
        'bundle', 'container_state', 'cancel_probability', 
        'cancel_risk', 'broken_route_probability', 
        'broken_route_risk', 'created_at'
    ]
    
    # Handle missing columns
    for col in columns:
        if col not in df_insert.columns:
            if col == 'booking_id':
                df_insert[col] = df_insert.index.astype(str)
            elif col == 'created_at':
                df_insert[col] = datetime.now()
            else:
                df_insert[col] = None
    
    df_insert = df_insert[columns]
    
    # Remove duplicates if replace_duplicates is True
    if replace_duplicates and 'booking_id' in df_insert.columns:
        # Get existing booking_ids
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT booking_id FROM bookings_scored WHERE booking_id IS NOT NULL')
        existing_ids = {row[0] for row in cursor.fetchall()}
        
        # Remove rows that already exist
        if existing_ids:
            df_insert = df_insert[~df_insert['booking_id'].isin(existing_ids)]
    
    # Insert into database
    if len(df_insert) > 0:
        df_insert.to_sql('bookings_scored', conn, if_exists='append', index=False)
        conn.commit()
    
    conn.close()


def query_scored_bookings(filters=None):
    """Query scored bookings with optional filters."""
    conn = sqlite3.connect(DATABASE_PATH)
    
    query = "SELECT * FROM bookings_scored WHERE 1=1"
    params = []
    
    if filters:
        if filters.get('start_date'):
            query += " AND booking_date >= ?"
            params.append(filters['start_date'])
        if filters.get('end_date'):
            query += " AND booking_date <= ?"
            params.append(filters['end_date'])
        if filters.get('lane'):
            query += " AND lane = ?"
            params.append(filters['lane'])
        if filters.get('pol'):
            query += " AND pol = ?"
            params.append(filters['pol'])
        if filters.get('pod'):
            query += " AND pod = ?"
            params.append(filters['pod'])
        if filters.get('month'):
            query += " AND strftime('%m', booking_date) = ?"
            params.append(f"{int(filters['month']):02d}")
        if filters.get('year'):
            query += " AND strftime('%Y', booking_date) = ?"
            params.append(str(filters['year']))
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return df


def get_filter_options():
    """Get available filter options from database."""
    conn = sqlite3.connect(DATABASE_PATH)
    
    options = {
        'lanes': pd.read_sql_query(
            "SELECT DISTINCT lane FROM bookings_scored WHERE lane IS NOT NULL ORDER BY lane", 
            conn
        )['lane'].tolist(),
        'pols': pd.read_sql_query(
            "SELECT DISTINCT pol FROM bookings_scored WHERE pol IS NOT NULL ORDER BY pol", 
            conn
        )['pol'].tolist(),
        'pods': pd.read_sql_query(
            "SELECT DISTINCT pod FROM bookings_scored WHERE pod IS NOT NULL ORDER BY pod", 
            conn
        )['pod'].tolist(),
        'years': pd.read_sql_query(
            "SELECT DISTINCT strftime('%Y', booking_date) as year FROM bookings_scored ORDER BY year DESC", 
            conn
        )['year'].tolist(),
    }
    
    conn.close()
    return options


def clear_database():
    """Clear all records from bookings_scored."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookings_scored')
    conn.commit()
    conn.close()