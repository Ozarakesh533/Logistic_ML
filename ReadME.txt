# Logistics ML Platform - Advanced Analytics Dashboard

## 📋 Overview

A complete end-to-end machine learning system for logistics booking risk prediction with an advanced analytics dashboard. This platform predicts:
- **Cancellation Risk**: Probability of a booking being cancelled
- **Broken Route Risk**: Probability of route disruption

The system includes a modern web interface with real-time data visualization, filtering capabilities, and comprehensive analytics.

---

## 🏗️ Project Structure

```
project_root/
│
├── artifacts/                    # All ML artifacts and database
│   ├── data_ingestion/           # Training/test data splits
│   ├── data_validation/          # Data quality reports
│   ├── data_transformation/      # Preprocessing pipelines (encoder.pkl)
│   ├── model_trainer/            # Trained ML models
│   │   ├── cancel_model.pkl
│   │   └── broken_route_model.pkl
│   ├── model_evaluation/         # Model performance metrics
│   └── logistics.db              # SQLite database (bookings_scored table)
│
├── mlProject/                    # ML pipelines and components
│   ├── components/               # Core ML components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_service.py      # Central prediction service
│   ├── pipeline/                 # ML pipelines
│   ├── constants/                # Configuration constants
│   └── utils/                    # Utility functions
│
├── backend/                      # Flask web application backend
│   ├── __init__.py               # App factory (creates Flask app)
│   ├── routes_pages.py           # HTML page routes (dashboard, predict, etc.)
│   └── routes_api.py             # JSON API endpoints for frontend
│
├── core/                         # Core prediction services
│   └── predictor.py             # Unified ML predictor
│
├── services/                      # Business logic services
│   ├── ingestion.py              # Data ingestion (CSV, Excel, JSON)
│   └── analytics.py              # Analytics and visualization data
│
├── database/                      # Database layer
│   └── database/
│       └── models.py             # Database models and queries
│
├── templates/                    # HTML templates (Jinja2)
│   ├── base.html                 # Base template with sidebar
│   ├── dashboard.html            # Advanced analytics dashboard
│   ├── predict.html              # Single prediction page
│   ├── bulk_predict.html         # Bulk prediction page
│   └── models.html               # Model metrics page
│
├── data/                         # Sample data directory
│   └── logistics_data.csv        # Sample logistics data
│
├── app.py                        # Flask application entry point
├── train_model.py                # ML model training script
├── generate_sample_data.py       # Generate synthetic sample data
├── populate_database.py          # Populate database with predictions
├── cleanup_database.py           # Remove duplicate records
├── requirements.txt              # Python dependencies
└── ReadME                        # This file
```

---

## 🛠️ Technology Stack

### Frontend Technologies

The user interface is built using modern web technologies:

1. **HTML5 & CSS3**
   - Semantic HTML structure
   - Custom CSS for styling and layout
   - Responsive design for different screen sizes

2. **Bootstrap 5.3.0** (via CDN)
   - **Purpose**: Provides responsive grid system, components, and utilities
   - **Used for**: Layout, cards, buttons, forms, navigation
   - **Location**: `templates/base.html` (loaded from CDN)
   - **Why**: Makes the UI professional and mobile-friendly without writing custom CSS

3. **Plotly.js 2.26.0** (via CDN)
   - **Purpose**: Interactive data visualization library
   - **Used for**: All charts and graphs (bar charts, line charts, heatmaps, Sankey diagrams, etc.)
   - **Location**: `templates/base.html` and `templates/dashboard.html`
   - **Why**: Provides interactive, professional charts that users can zoom, pan, and hover on

4. **Font Awesome 6.4.0** (via CDN)
   - **Purpose**: Icon library
   - **Used for**: Icons in sidebar navigation, buttons, and UI elements
   - **Location**: `templates/base.html`
   - **Why**: Adds visual icons to improve user experience

5. **JavaScript (Vanilla JS)**
   - **Purpose**: Client-side interactivity
   - **Used for**: 
     - Fetching data from API endpoints
     - Updating charts when filters change
     - Dynamic form handling
     - Real-time dashboard updates
   - **Location**: Embedded in `templates/dashboard.html` and other template files
   - **Why**: No framework needed - simple, fast, and lightweight

6. **Jinja2 Template Engine**
   - **Purpose**: Server-side templating (comes with Flask)
   - **Used for**: Dynamic HTML generation, template inheritance
   - **Location**: All files in `templates/` directory
   - **Why**: Allows reusable templates and dynamic content

### Backend Technologies

The server-side is built with Python and Flask:

1. **Flask 3.0+** (Python Web Framework)
   - **Purpose**: Web application framework
   - **Used for**: 
     - Routing (handling URLs)
     - Rendering HTML templates
     - Serving JSON API endpoints
     - File uploads (bulk prediction)
   - **Location**: `backend/` directory, `app.py`
   - **Why**: Lightweight, flexible, perfect for ML applications

2. **SQLite Database**
   - **Purpose**: Persistent data storage
   - **Used for**: Storing scored bookings in `bookings_scored` table
   - **Location**: `artifacts/logistics.db`
   - **Why**: Simple, file-based database - no separate server needed
   - **Schema**: See `database/database/models.py` for table structure

3. **Pandas 2.0+** (Data Manipulation)
   - **Purpose**: Data processing and analysis
   - **Used for**: 
     - Reading CSV/Excel/JSON files
     - Data transformation
     - Database queries
     - Data aggregation for charts
   - **Location**: Used throughout `services/`, `backend/`, `core/`

4. **NumPy 1.24+** (Numerical Computing)
   - **Purpose**: Mathematical operations
   - **Used for**: Array operations, numerical computations
   - **Location**: Used in ML components

5. **scikit-learn 1.3+** (Machine Learning)
   - **Purpose**: ML algorithms and preprocessing
   - **Used for**: 
     - Logistic Regression
     - Random Forest
     - Data preprocessing (OneHotEncoder, StandardScaler)
     - Model evaluation metrics
   - **Location**: `mlProject/components/`

6. **XGBoost 2.0+** (Gradient Boosting)
   - **Purpose**: Advanced ML algorithm
   - **Used for**: Training high-performance models
   - **Location**: `mlProject/components/model_trainer.py`

7. **Joblib** (Model Serialization)
   - **Purpose**: Save and load trained models
   - **Used for**: Persisting `.pkl` model files
   - **Location**: Model saving/loading in `mlProject/components/`

8. **openpyxl 3.1+** (Excel Support)
   - **Purpose**: Read/write Excel files
   - **Used for**: Processing `.xlsx` and `.xls` files in bulk prediction
   - **Location**: `services/ingestion.py`

---

## 📦 Installation & Setup

### Step 1: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning algorithms
- `xgboost` - Gradient boosting models
- `Flask` - Web framework
- `joblib` - Model serialization
- `openpyxl` - Excel file support
- `python-dateutil` - Date handling
- `pytest` - Testing framework

### Step 2: Prepare Sample Data

You have two options:

#### Option A: Generate Sample Data (Recommended for Testing)

```bash
python generate_sample_data.py
```

**What this does:**
- Creates `data/logistics_data.csv` with 5,000 synthetic booking records
- Includes realistic logistics data (ports, lanes, dates, etc.)
- Generates target variables (cancel, broken_route) with realistic patterns

#### Option B: Use Your Own Data

Place your CSV file at `data/logistics_data.csv` with these columns:
- **Required**: `pol`, `lane`, `container_state`, `cancel`, `broken_route`
- **Optional**: `pod`, `bundle`, `booking_date`, `booking_no`

### Step 3: Train ML Models

```bash
python train_model.py
```

**What this does:**
1. Loads data from `data/logistics_data.csv`
2. Splits into training (80%) and testing (20%) sets
3. Validates data quality
4. Engineers features (extracts year, month, day from dates)
5. Transforms categorical variables (OneHot encoding)
6. Trains multiple models:
   - Logistic Regression
   - Random Forest
   - XGBoost
7. Selects best model based on F1 score and AUC
8. Saves models to `artifacts/model_trainer/`
9. Generates performance metrics

**Output files:**
- `artifacts/model_trainer/cancel_model.pkl` - Cancellation prediction model
- `artifacts/model_trainer/broken_route_model.pkl` - Broken route prediction model
- `artifacts/data_transformation/encoder.pkl` - Data preprocessing pipeline
- `artifacts/model_evaluation/metrics.json` - Model performance metrics

### Step 4: Populate Database with Sample Data

**This is important!** The dashboard reads from the database, not from CSV files.

```bash
python populate_database.py
```

**What this does:**
1. Initializes SQLite database (`artifacts/logistics.db`)
2. Creates `bookings_scored` table if it doesn't exist
3. Loads sample data from `data/logistics_data.csv`
4. Processes data through ingestion service (standardizes column names)
5. Generates predictions using trained ML models
6. Saves all records with predictions to database

**Result:** Database now contains scored bookings that the dashboard can display.

**Note:** If you see duplicate records, run:
```bash
python cleanup_database.py
```

### Step 5: Start the Web Application

```bash
python app.py
```

**What happens:**
- Flask server starts on `http://localhost:5000`
- Database is initialized automatically
- ML models are loaded into memory
- Application is ready to serve requests

**Or use the batch file (Windows):**
```bash
run_app.bat
```

**Or use automated setup (Windows):**
```bash
setup_and_run.bat
```
This will do steps 2-5 automatically!

---

## 🎯 Features & Pages

### 1. Dashboard (Advanced Analytics)

**URL:** `http://localhost:5000/dashboard`

**Features:**
- **Filter Bar**: Filter by date range, month, year, lane, or port
- **KPI Cards**: 
  - Total Bookings
  - Cancel Rate (%)
  - Broken Route Rate (%)
  - Unique Lanes
- **Overview Charts**:
  - Cancellations by Lane (bar chart)
  - Cancellations by Port (bar chart)
  - Bookings Over Time (line chart)
- **Flow & Movement Visuals**:
  - Sankey Diagram (Lane → State → Risk flow)
  - Chord Diagram (POL ↔ POD connections)
  - Flow Map (volume visualization)
- **Seasonality & Time Patterns**:
  - Calendar Heatmap (daily cancellation rates)
  - Ridgeline Plot (volume over time per lane)
  - Stacked Area Chart (bookings by lane over time)
  - Cancel Rate Over Time
- **Utilization & Performance**:
  - Waffle Chart (container state distribution)
  - Risk Distribution (pie chart)
- **Risk & Exceptions**:
  - Risk Matrix Heatmap (Port × Lane)
  - Top 5 Risky Lanes
  - Top 5 Risky Ports
  - Top Outliers Table (highest-risk bookings)

**How it works:**
- Frontend JavaScript calls API endpoints when filters change
- Backend queries database and returns JSON data
- Plotly.js renders interactive charts
- All charts update automatically when filters are applied

### 2. Single Prediction

**URL:** `http://localhost:5000/predict`

**Features:**
- Input form for individual booking details
- Real-time risk predictions
- Visual risk indicators (Low/Medium/High badges)
- Probability bars showing cancellation and broken route risks

**How it works:**
- User fills form and clicks "Predict"
- JavaScript sends POST request to `/api/predict`
- Backend uses `ModelService` to generate predictions
- Results displayed with color-coded risk levels

### 3. Bulk Prediction

**URL:** `http://localhost:5000/bulk-predict`

**Features:**
- Upload CSV, Excel (.xlsx, .xls), or JSON files
- Process multiple bookings at once
- Preview results in table
- Download augmented CSV with predictions
- **Automatically saves to database** for dashboard visualization

**How it works:**
1. User uploads file
2. `DataIngestionService` reads and standardizes columns
3. `UnifiedPredictor` generates predictions for all records
4. Results saved to `bookings_scored` table
5. Preview shown and CSV download offered

### 4. Model Metrics

**URL:** `http://localhost:5000/models`

**Features:**
- View model performance metrics
- Compare cancel vs broken route models
- Metrics include: Accuracy, Precision, Recall, F1 Score, AUC-ROC

---

## 🔌 API Endpoints

All API endpoints return JSON data and support filtering via query parameters.

### Dashboard Endpoints

- `GET /api/dashboard-summary` - Get KPI statistics
  - Query params: `start_date`, `end_date`, `month`, `year`, `lane`, `pol`
  
- `GET /api/bookings-over-time` - Get bookings aggregated over time
  - Query params: Same as above + `freq` (D/M/Y for daily/monthly/yearly)

- `GET /api/cancellations-by-port` - Get cancellation rates by port
  - Query params: Filters + `top_n` (default: 10)

- `GET /api/cancellations-by-lane` - Get cancellation rates by lane
  - Query params: Filters + `top_n` (default: 10)

- `GET /api/risk-distribution` - Get risk level distribution
  - Query params: Filters

- `GET /api/flow-data` - Get data for Sankey diagram
  - Query params: Filters

- `GET /api/seasonality-data` - Get data for calendar heatmap
  - Query params: Filters

- `GET /api/network-data` - Get data for chord diagram
  - Query params: Filters

- `GET /api/risk-matrix` - Get risk matrix heatmap data
  - Query params: Filters

- `GET /api/ridgeline-data` - Get ridgeline plot data
  - Query params: Filters

- `GET /api/stacked-area-data` - Get stacked area chart data
  - Query params: Filters

- `GET /api/waffle-data` - Get waffle chart data
  - Query params: Filters

- `GET /api/top-risky-lanes` - Get top risky lanes
  - Query params: Filters + `top_n` (default: 5)

- `GET /api/top-risky-ports` - Get top risky ports
  - Query params: Filters + `top_n` (default: 5)

- `GET /api/top-outliers` - Get highest-risk bookings
  - Query params: Filters + `top_n` (default: 10)

- `GET /api/filter-options` - Get available filter values
  - Returns: Available lanes, ports, years for dropdowns

### Prediction Endpoints

- `POST /api/predict` - Single booking prediction
  ```json
  {
    "lane": "TRANSPACIFIC",
    "pol": "SHANGHAI",
    "pod": "LOS_ANGELES",
    "container_state": "FCL",
    "bundle": "STANDARD",
    "booking_date": "2024-01-15"
  }
  ```

- `POST /api/bulk-predict` - Bulk CSV/Excel/JSON prediction
  - Upload file as `multipart/form-data` with key `file`
  - Returns: Preview, total records, and CSV download

### Legacy Endpoints (Still Supported)

- `GET /api/stats/overview` - Legacy KPI endpoint
- `GET /api/stats/charts` - Legacy chart data endpoint

---

## 💾 Database Schema

The `bookings_scored` table stores all predictions:

```sql
CREATE TABLE bookings_scored (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id TEXT,
    booking_date DATE,
    pol TEXT,                    -- Port of Loading
    pod TEXT,                    -- Port of Discharge
    lane TEXT,                   -- Trade Lane
    bundle TEXT,                 -- Bundle Type
    container_state TEXT,         -- FCL, LCL, EMPTY
    cancel_probability REAL,      -- 0.0 to 1.0
    cancel_risk TEXT,            -- Low, Medium, High
    broken_route_probability REAL, -- 0.0 to 1.0
    broken_route_risk TEXT,      -- Low, Medium, High
    created_at TIMESTAMP         -- When record was created
);
```

**Indexes created for performance:**
- `idx_booking_date` - Fast date filtering
- `idx_lane` - Fast lane filtering
- `idx_pol` - Fast port filtering
- `idx_pod` - Fast destination filtering
- `idx_created_at` - Fast time-based queries

---

## 🔄 Data Flow

### How Data Gets Into the Dashboard

1. **Initial Setup:**
   ```
   generate_sample_data.py → data/logistics_data.csv
   train_model.py → artifacts/model_trainer/*.pkl
   populate_database.py → artifacts/logistics.db (bookings_scored table)
   ```

2. **Bulk Prediction Flow:**
   ```
   User uploads file → DataIngestionService.ingest()
   → UnifiedPredictor.predict_bookings()
   → insert_scored_bookings() → Database
   → Dashboard reads from database
   ```

3. **Dashboard Display Flow:**
   ```
   User applies filters → JavaScript fetch() → API endpoint
   → query_scored_bookings(filters) → Database query
   → AnalyticsService processes data → JSON response
   → Plotly.js renders charts
   ```

---

## 🎨 Customization

### Changing Column Names

If your data has different column names, edit `services/ingestion.py`:

```python
COLUMN_MAPPING = {
    'your_booking_no': 'booking_id',
    'your_origin': 'pol',
    'your_destination': 'pod',
    # ... etc
}
```

### Adding New Features

1. Update `mlProject/constants/__init__.py`:
   ```python
   CATEGORICAL_FEATURES = ["pol", "pod", "lane", "new_feature"]
   ```

2. Retrain models: `python train_model.py`

### Adding New Visualizations

1. Add method to `services/analytics.py`
2. Add API endpoint in `backend/routes_api.py`
3. Add chart div and JavaScript in `templates/dashboard.html`

---

## 🐛 Troubleshooting

### Dashboard Shows Empty/Zero Values

**Problem:** Database is empty or not populated.

**Solution:**
```bash
python populate_database.py
```

### Models Not Loading

**Problem:** Model files missing or version mismatch.

**Solution:**
```bash
python train_model.py
```

### Duplicate Records in Database

**Problem:** Data inserted multiple times.

**Solution:**
```bash
python cleanup_database.py
```

### Charts Not Displaying

**Problem:** JavaScript errors or API failures.

**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify Flask app is running
4. Check API endpoints return data: `http://localhost:5000/api/dashboard-summary`

### Port 5000 Already in Use

**Solution:** Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📊 Example Usage

### Generate Sample Data
```bash
python generate_sample_data.py
# Creates data/logistics_data.csv with 5,000 records
```

### Train Models
```bash
python train_model.py
# Trains and saves models to artifacts/model_trainer/
```

### Populate Database
```bash
python populate_database.py
# Processes data, generates predictions, saves to database
```

### Start Application
```bash
python app.py
# Server starts on http://localhost:5000
```

### Access Dashboard
Open browser: `http://localhost:5000`

---

## 🔐 Production Deployment

Before deploying to production:

1. **Security:**
   - Change `SECRET_KEY` in `backend/__init__.py`
   - Add authentication/authorization
   - Enable HTTPS
   - Validate all inputs

2. **Performance:**
   - Use production WSGI server (gunicorn/uwsgi)
   - Add caching (Redis)
   - Consider PostgreSQL instead of SQLite
   - Load balancing for high traffic

3. **Monitoring:**
   - Add logging to files
   - Set up error tracking (Sentry)
   - Monitor model performance
   - A/B testing for model versions

---

## 📝 File Descriptions

### Key Files

- **`app.py`** - Flask application entry point
- **`train_model.py`** - ML model training script
- **`generate_sample_data.py`** - Creates synthetic test data
- **`populate_database.py`** - Populates database with predictions
- **`cleanup_database.py`** - Removes duplicate records
- **`backend/routes_api.py`** - All API endpoints
- **`backend/routes_pages.py`** - HTML page routes
- **`services/ingestion.py`** - File reading and standardization
- **`services/analytics.py`** - Analytics calculations
- **`core/predictor.py`** - Unified prediction service
- **`database/database/models.py`** - Database operations

---

## 🤝 Support

For issues or questions:
1. Check console logs for errors
2. Verify data format matches expected schema
3. Ensure models are trained (`artifacts/model_trainer/*.pkl` exists)
4. Check database has data (`python populate_database.py`)
5. Review configuration in `mlProject/constants/__init__.py`

---

## 📄 License

MIT License - feel free to use for your projects!

---

**Built with ❤️ for modern logistics optimization**

*Last Updated: 2025*
