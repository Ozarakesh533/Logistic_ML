# ============================================================================
# FILE: test_prediction.py
# ============================================================================
"""
Test script for predictions without running the web app.
"""
from mlProject.components.model_service import ModelService
import pandas as pd


def test_single_prediction():
    """Test single booking prediction."""
    print("\n" + "="*60)
    print("Testing Single Prediction")
    print("="*60)
    
    # Initialize service
    service = ModelService()
    service.load_models()
    
    # Create sample booking
    booking = pd.DataFrame([{
        'lane': 'TRANSPACIFIC',
        'pol': 'SHANGHAI',
        'pod': 'LOS_ANGELES',
        'destination': 'LOS_ANGELES',
        'container_state': 'FCL',
        'bundle': 'STANDARD',
        'booking_date': '2024-01-15',
        'origin_id': 10,
        'destination_id': 20
    }])
    
    print("\nInput booking:")
    print(booking.to_string(index=False))
    
    # Predict
    results = service.predict_all(booking)
    
    print("\n" + "-"*60)
    print("Prediction Results:")
    print("-"*60)
    print(f"\n📦 Cancellation Risk:")
    print(f"  Probability: {results[0]['cancel']['probability']*100:.2f}%")
    print(f"  Risk Level:  {results[0]['cancel']['risk_label']}")
    
    print(f"\n🚨 Broken Route Risk:")
    print(f"  Probability: {results[0]['broken_route']['probability']*100:.2f}%")
    print(f"  Risk Level:  {results[0]['broken_route']['risk_label']}")


def test_bulk_prediction():
    """Test bulk predictions."""
    print("\n" + "="*60)
    print("Testing Bulk Prediction")
    print("="*60)
    
    # Initialize service
    service = ModelService()
    service.load_models()
    
    # Create sample bookings
    bookings = pd.DataFrame([
        {
            'lane': 'TRANSPACIFIC',
            'pol': 'SHANGHAI',
            'pod': 'LOS_ANGELES',
            'destination': 'LOS_ANGELES',
            'container_state': 'FCL',
            'bundle': 'STANDARD',
            'booking_date': '2024-01-15',
            'origin_id': 10,
            'destination_id': 20
        },
        {
            'lane': 'INTRA_ASIA',
            'pol': 'SINGAPORE',
            'pod': 'TOKYO',
            'destination': 'TOKYO',
            'container_state': 'LCL',
            'bundle': 'ECO',
            'booking_date': '2024-02-20',
            'origin_id': 15,
            'destination_id': 25
        },
        {
            'lane': 'TRANSATLANTIC',
            'pol': 'HAMBURG',
            'pod': 'NEW_YORK',
            'destination': 'NEW_YORK',
            'container_state': 'EMPTY',
            'bundle': 'PREMIUM',
            'booking_date': '2024-03-10',
            'origin_id': 30,
            'destination_id': 35
        }
    ])
    
    print(f"\nProcessing {len(bookings)} bookings...")
    
    # Predict
    results = service.predict_all(bookings)
    
    # Add results to dataframe
    bookings['cancel_prob'] = [r['cancel']['probability']*100 for r in results]
    bookings['cancel_risk'] = [r['cancel']['risk_label'] for r in results]
    bookings['broken_prob'] = [r['broken_route']['probability']*100 for r in results]
    bookings['broken_risk'] = [r['broken_route']['risk_label'] for r in results]
    
    print("\n" + "-"*60)
    print("Results Summary:")
    print("-"*60)
    print(bookings[['lane', 'pol', 'pod', 'cancel_prob', 'cancel_risk', 
                     'broken_prob', 'broken_risk']].to_string(index=False))


def main():
    """Run all tests."""
    try:
        test_single_prediction()
        test_bulk_prediction()
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60)
        
    except FileNotFoundError:
        print("\n❌ Error: Models not found!")
        print("Please train the models first by running:")
        print("  python train_model.py")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()