# ============================================================================
# FILE: cleanup_database.py
# ============================================================================
"""
Clean up duplicate records from the database.
Keeps only the most recent record for each booking_id.
"""
import sqlite3
import os
from mlProject.constants import ARTIFACTS_DIR

DATABASE_PATH = os.path.join(ARTIFACTS_DIR, 'logistics.db')


def cleanup_duplicates():
    """Remove duplicate records, keeping the most recent one for each booking_id."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Count before
    cursor.execute('SELECT COUNT(*) FROM bookings_scored')
    count_before = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT booking_id) FROM bookings_scored WHERE booking_id IS NOT NULL')
    unique_before = cursor.fetchone()[0]
    
    print(f"Records before cleanup: {count_before}")
    print(f"Unique booking_ids: {unique_before}")
    
    # Delete duplicates, keeping the one with the highest id (most recent)
    # Handle NULL booking_ids separately
    cursor.execute('''
        DELETE FROM bookings_scored
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM bookings_scored
            WHERE booking_id IS NOT NULL
            GROUP BY booking_id
        )
        AND booking_id IS NOT NULL
    ''')
    
    deleted = cursor.rowcount
    conn.commit()
    
    # Also remove duplicate NULL booking_ids (keep only one)
    cursor.execute('''
        DELETE FROM bookings_scored
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM bookings_scored
            WHERE booking_id IS NULL
        )
        AND booking_id IS NULL
    ''')
    
    deleted_null = cursor.rowcount
    conn.commit()
    
    # Count after
    cursor.execute('SELECT COUNT(*) FROM bookings_scored')
    count_after = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT booking_id) FROM bookings_scored WHERE booking_id IS NOT NULL')
    unique_after = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"Deleted {deleted} duplicate records (with booking_id)")
    if deleted_null > 0:
        print(f"Deleted {deleted_null} duplicate NULL booking_id records")
    print(f"Records after cleanup: {count_after}")
    print(f"Unique booking_ids: {unique_after}")
    print(f"✓ Database cleaned up successfully!")
    
    return count_after


if __name__ == '__main__':
    cleanup_duplicates()

