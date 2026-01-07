# 🚀 Quick Start Guide - Logistics ML Dashboard

## Step-by-Step Instructions to Run and Visualize

### 1. Install Dependencies

```bash
# Activate virtual environment (if using one)
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Train ML Models (First Time Only)

If you haven't trained models yet:

```bash
# Generate sample data (if you don't have real data)
python generate_sample_data.py

# Train the ML models
python train_model.py
```

This creates model files in `artifacts/model_trainer/`:
- `cancel_model.pkl`
- `broken_route_model.pkl`
- `encoder.pkl`

### 3. Populate Database with Sample Data

The dashboard reads from the `bookings_scored` database table. To see visualizations, you need to populate it:

**Option A: Use Bulk Prediction (Recommended)**
1. Generate sample data: `python generate_sample_data.py`
2. Start the app: `python app.py`
3. Go to **Bulk Prediction** page
4. Upload `data/logistics_data.csv`
5. The predictions will be automatically saved to the database

**Option B: Use the Helper Script**
```bash
python populate_database.py
```

This script will:
- Generate sample data
- Run predictions
- Save to database automatically

### 4. Start the Flask Application

```bash
python app.py
```

You should see:
```
INFO - Models loaded successfully!
INFO - Database initialized successfully!
 * Running on http://0.0.0.0:5000
```

### 5. Access the Dashboard

Open your browser and go to:
```
http://localhost:5000
```

You'll be automatically redirected to the **Dashboard** page.

## 📊 Using the Dashboard

### Filter Controls

At the top of the dashboard, you'll find filter controls:
- **Start Date / End Date**: Filter by date range
- **Month**: Filter by specific month
- **Year**: Filter by specific year
- **Lane**: Filter by trade lane
- **Port**: Filter by port of loading

**To apply filters:**
1. Select your desired filters
2. Click **"Apply Filters"** button
3. All charts and KPIs will update automatically

**To clear filters:**
- Click **"Clear"** button to reset all filters

### Dashboard Sections

1. **Overview Charts** (Original)
   - Cancellations by Lane
   - Cancellations by Port
   - Bookings Over Time

2. **Flow & Movement Visuals**
   - Sankey Diagram: Shows flow from Lane → Container State → Risk
   - Chord Diagram: POL ↔ POD flow matrix
   - Flow Map: Volume visualization over time

3. **Seasonality & Time Patterns**
   - Calendar Heatmap: Daily cancellation rates
   - Ridgeline Plot: Volume over time per lane
   - Stacked Area Chart: Bookings over time grouped by lane
   - Cancel Rate Over Time: Line chart showing trends

4. **Utilization & Performance**
   - Waffle Chart: Container state distribution
   - Risk Distribution: Pie chart of risk levels

5. **Risk & Exceptions**
   - Risk Matrix Heatmap: Port × Lane risk analysis
   - Top 5 Risky Lanes: Bar chart
   - Top 5 Risky Ports: Bar chart
   - Top Outliers Table: Highest-risk bookings

## 🔍 Troubleshooting

### Empty Dashboard / No Data

If you see empty charts or "0" values:
1. Make sure you've populated the database (Step 3)
2. Check that models are trained (Step 2)
3. Verify the database file exists: `artifacts/logistics.db`

### Models Not Loading

If you see warnings about models:
1. Run `python train_model.py` to train models
2. Check that these files exist:
   - `artifacts/model_trainer/cancel_model.pkl`
   - `artifacts/model_trainer/broken_route_model.pkl`
   - `artifacts/data_transformation/encoder.pkl`

### Database Errors

The database auto-initializes on startup. If you see database errors:
1. Check file permissions in the `artifacts/` directory
2. Delete `artifacts/logistics.db` and restart (it will recreate)

## 📝 Quick Test

To quickly test everything:

```bash
# 1. Generate sample data
python generate_sample_data.py

# 2. Train models (if not done)
python train_model.py

# 3. Populate database
python populate_database.py

# 4. Start app
python app.py

# 5. Open browser
# http://localhost:5000
```

## 🎯 Next Steps

- **Single Prediction**: Test individual booking predictions
- **Bulk Prediction**: Upload CSV/Excel files for batch processing
- **Model Metrics**: View model performance metrics
- **Customize**: Modify filters, add new visualizations, or integrate real data

Enjoy exploring your logistics analytics! 🚢📊

