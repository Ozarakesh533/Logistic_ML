# ============================================================================
# FILE: generate_sample_data.py
# ============================================================================
"""
Generate sample logistics data for testing.
Run this if you don't have real data yet.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

def generate_sample_data(n_samples=5000):
    """Generate synthetic logistics booking data."""
    
    # Define categories
    lanes = ['TRANSPACIFIC', 'TRANSATLANTIC', 'INTRA_ASIA', 'EUROPE_ASIA', 
             'MIDDLE_EAST', 'LATIN_AMERICA', 'AFRICA', 'OCEANIA']
    
    ports_origin = ['SHANGHAI', 'SINGAPORE', 'HONG_KONG', 'ROTTERDAM', 
                    'HAMBURG', 'DUBAI', 'LOS_ANGELES', 'TOKYO', 'MUMBAI']
    
    ports_dest = ['LOS_ANGELES', 'NEW_YORK', 'ROTTERDAM', 'HAMBURG', 
                  'SINGAPORE', 'TOKYO', 'SHANGHAI', 'DUBAI', 'SYDNEY']
    
    container_states = ['FCL', 'LCL', 'EMPTY']
    bundles = ['STANDARD', 'PREMIUM', 'EXPRESS', 'ECO']
    
    # Generate base data
    data = {
        'booking_no': [f'BK{str(i).zfill(8)}' for i in range(1, n_samples + 1)],
        'lane': np.random.choice(lanes, n_samples),
        'pol': np.random.choice(ports_origin, n_samples),
        'pod': np.random.choice(ports_dest, n_samples),
        'destination': np.random.choice(ports_dest, n_samples),
        'container_state': np.random.choice(container_states, n_samples),
        'bundle': np.random.choice(bundles, n_samples),
        'origin_id': np.random.randint(1, 100, n_samples),
        'destination_id': np.random.randint(1, 100, n_samples)
    }
    
    # Generate booking dates (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    booking_dates = [start_date + timedelta(days=np.random.randint(0, 730)) 
                     for _ in range(n_samples)]
    data['booking_date'] = [d.strftime('%Y-%m-%d') for d in booking_dates]
    
    df = pd.DataFrame(data)
    
    # Generate targets with some logic (not purely random)
    # Cancellation logic: higher for certain lanes and container states
    cancel_prob = 0.15  # base 15% cancellation rate
    df['cancel_base_prob'] = cancel_prob
    
    # Increase cancel probability for specific conditions
    df.loc[df['lane'] == 'TRANSPACIFIC', 'cancel_base_prob'] *= 1.5
    df.loc[df['container_state'] == 'EMPTY', 'cancel_base_prob'] *= 1.3
    df.loc[df['bundle'] == 'ECO', 'cancel_base_prob'] *= 1.2
    
    # Generate cancel target
    df['cancel'] = (np.random.random(n_samples) < df['cancel_base_prob']).astype(int)
    
    # Broken route logic: higher for longer routes and certain ports
    broken_prob = 0.12  # base 12% broken route rate
    df['broken_base_prob'] = broken_prob
    
    df.loc[df['lane'].isin(['TRANSPACIFIC', 'TRANSATLANTIC']), 'broken_base_prob'] *= 1.4
    df.loc[df['pol'].isin(['SHANGHAI', 'HONG_KONG']), 'broken_base_prob'] *= 1.2
    df.loc[df['container_state'] == 'FCL', 'broken_base_prob'] *= 0.9
    
    # Generate broken_route target
    df['broken_route'] = (np.random.random(n_samples) < df['broken_base_prob']).astype(int)
    
    # Drop temporary probability columns
    df = df.drop(['cancel_base_prob', 'broken_base_prob'], axis=1)
    
    # Add some missing values to make it realistic
    missing_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    df.loc[missing_indices, 'bundle'] = np.nan
    
    missing_indices = np.random.choice(n_samples, size=int(n_samples * 0.02), replace=False)
    df.loc[missing_indices, 'destination_id'] = np.nan
    
    return df


def main():
    """Generate and save sample data."""
    print("Generating sample logistics data...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate data
    df = generate_sample_data(n_samples=5000)
    
    # Save
    output_path = 'data/logistics_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Sample data generated successfully!")
    print(f"  Location: {output_path}")
    print(f"  Total records: {len(df)}")
    print(f"\nData Summary:")
    print(f"  Cancellation rate: {df['cancel'].mean()*100:.2f}%")
    print(f"  Broken route rate: {df['broken_route'].mean()*100:.2f}%")
    print(f"  Unique lanes: {df['lane'].nunique()}")
    print(f"  Unique ports (origin): {df['pol'].nunique()}")
    print(f"  Unique ports (dest): {df['pod'].nunique()}")
    print(f"\nYou can now run: python train_model.py")


if __name__ == '__main__':
    main()