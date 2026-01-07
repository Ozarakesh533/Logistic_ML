# ============================================================================
# FILE: populate_database.py
# ============================================================================
"""
Helper script to populate the database with sample data and predictions.
Run this to quickly set up the dashboard with data.
"""
import pandas as pd
import os
import sys
from services.ingestion import DataIngestionService
from core.predictor import UnifiedPredictor
from database.database.models import init_database, insert_scored_bookings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """Populate database with sample data."""
    print("=" * 60)
    print("Populating Database with Sample Data")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    try:
        init_database()
        print("   ✓ Database initialized")
    except Exception as e:
        print(f"   ✗ Error initializing database: {e}")
        return
    
    # Check if sample data exists
    sample_data_path = 'data/logistics_data.csv'
    if not os.path.exists(sample_data_path):
        print(f"\n2. Sample data not found at {sample_data_path}")
        print("   Generating sample data...")
        try:
            from generate_sample_data import generate_sample_data
            os.makedirs('data', exist_ok=True)
            df = generate_sample_data(n_samples=5000)
            df.to_csv(sample_data_path, index=False)
            print(f"   ✓ Generated {len(df)} sample records")
        except Exception as e:
            print(f"   ✗ Error generating sample data: {e}")
            return
    else:
        print(f"\n2. Found sample data at {sample_data_path}")
        df = pd.read_csv(sample_data_path)
        print(f"   ✓ Loaded {len(df)} records")
    
    # Initialize services
    print("\n3. Initializing ML services...")
    try:
        ingestion_service = DataIngestionService()
        predictor = UnifiedPredictor()
        predictor.load_models()
        print("   ✓ Services initialized")
    except Exception as e:
        print(f"   ✗ Error initializing services: {e}")
        print("   Make sure models are trained. Run: python train_model.py")
        return
    
    # Ingest and standardize data
    print("\n4. Processing data...")
    try:
        df_processed = ingestion_service.ingest(sample_data_path)
        print(f"   ✓ Processed {len(df_processed)} records")
    except Exception as e:
        print(f"   ✗ Error processing data: {e}")
        return
    
    # Generate predictions
    print("\n5. Generating predictions...")
    try:
        df_enriched = predictor.predict_bookings(df_processed)
        print(f"   ✓ Generated predictions for {len(df_enriched)} bookings")
        print(f"   - Average cancel probability: {df_enriched['cancel_probability'].mean()*100:.2f}%")
        print(f"   - Average broken route probability: {df_enriched['broken_route_probability'].mean()*100:.2f}%")
    except Exception as e:
        print(f"   ✗ Error generating predictions: {e}")
        return
    
    # Save to database
    print("\n6. Saving to database...")
    try:
        # Check if database already has data
        from database.database.models import query_scored_bookings
        existing = query_scored_bookings()
        if len(existing) > 0:
            print(f"   ⚠ Database already has {len(existing)} records")
            response = input("   Do you want to replace duplicates? (y/n): ").strip().lower()
            if response == 'y':
                insert_scored_bookings(df_enriched, replace_duplicates=True)
                print(f"   ✓ Saved {len(df_enriched)} records (duplicates replaced)")
            else:
                print("   Skipping insert. Use cleanup_database.py to remove duplicates first.")
                return
        else:
            insert_scored_bookings(df_enriched)
            print(f"   ✓ Saved {len(df_enriched)} records to bookings_scored table")
    except Exception as e:
        print(f"   ✗ Error saving to database: {e}")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("✓ Database populated successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Open browser: http://localhost:5000")
    print("3. Explore the dashboard with filters and visualizations!")
    print("\n")


if __name__ == '__main__':
    main()

