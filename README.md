# Logistics ML Platform - Advanced Analytics Dashboard

## 📋 Overview

An end-to-end ML system for logistics booking risk prediction with an interactive analytics dashboard.

**Predicts:** Cancellation Risk | Broken Route Risk

🌐 **Live Demo:** [https://logistic-ml-2.onrender.com](https://logistic-ml-2.onrender.com)

---

## 🚀 Quick Start

### Try it Live
Visit the deployed application: **[https://logistic-ml-2.onrender.com](https://logistic-ml-2.onrender.com)**

### Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python generate_sample_data.py

# 3. Train models
python train_model.py

# 4. Populate database
python populate_database.py

# 5. Start application
python app.py
```

Open browser: `http://localhost:5000`

---

## 🏗️ Project Structure

```
project_root/
├── artifacts/                  # ML models, database, preprocessors
│   ├── model_trainer/*.pkl     # Trained models
│   └── logistics.db            # SQLite database
├── backend/                    # Flask app (routes, APIs)
├── core/                       # ML prediction service
├── services/                   # Data ingestion, analytics
├── database/                   # DB models and queries
├── templates/                  # HTML pages (Jinja2)
├── data/                       # Sample data
└── mlProject/                  # ML pipeline components
```

---

## 🛠️ Tech Stack

**Frontend:** Bootstrap 5.3 | Plotly.js | Vanilla JavaScript | Jinja2  
**Backend:** Flask 3.0 | SQLite | Pandas 2.0  
**ML:** scikit-learn 1.3 | XGBoost 2.0 | NumPy 1.24  
**Deployment:** Render

---

## 🎯 Features

### 1. **Dashboard** (`/dashboard`)
- KPI cards (Total bookings, cancel rate, broken route rate)
- 15+ interactive charts (bar, line, Sankey, heatmap, chord diagram)
- Advanced filters (date, lane, port)
- Real-time updates

### 2. **Single Prediction** (`/predict`)
- Form input for single booking
- Real-time risk predictions with visual indicators

### 3. **Bulk Prediction** (`/bulk-predict`)
- Upload CSV/Excel/JSON files
- Process multiple bookings
- Auto-save to database
- Download results

### 4. **Model Metrics** (`/models`)
- View model performance (Accuracy, F1, AUC-ROC)
- Compare models

---

## 🔌 Key API Endpoints

**Dashboard Data:**
- `/api/dashboard-summary` - KPIs
- `/api/bookings-over-time` - Time series
- `/api/cancellations-by-lane` - Lane analysis
- `/api/cancellations-by-port` - Port analysis
- `/api/risk-matrix` - Heatmap data
- `/api/top-risky-lanes` - High-risk lanes
- `/api/filter-options` - Available filters

**Predictions:**
- `POST /api/predict` - Single prediction
- `POST /api/bulk-predict` - Bulk upload

*All endpoints support filtering: `?start_date=2024-01-01&lane=TRANSPACIFIC`*

---

## 💾 Database Schema

```sql
CREATE TABLE bookings_scored (
    id INTEGER PRIMARY KEY,
    booking_id TEXT,
    booking_date DATE,
    pol TEXT,                      -- Port of Loading
    pod TEXT,                      -- Port of Discharge
    lane TEXT,
    container_state TEXT,
    cancel_probability REAL,       -- 0.0 to 1.0
    cancel_risk TEXT,              -- Low/Medium/High
    broken_route_probability REAL,
    broken_route_risk TEXT,
    created_at TIMESTAMP
);
```

---

## 🔄 Data Flow

```
CSV Upload → DataIngestion → ML Prediction → Database → Dashboard
```

---

## 🎨 Customization

**Change column names:** Edit `services/ingestion.py`
```python
COLUMN_MAPPING = {
    'your_origin': 'pol',
    'your_destination': 'pod'
}
```

**Add new features:** Update `mlProject/constants/__init__.py` → Retrain models

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Empty dashboard | Run `python populate_database.py` |
| Models not loading | Run `python train_model.py` |
| Duplicate records | Run `python cleanup_database.py` |
| Port 5000 in use | Change port in `app.py` |
| Charts not showing | Check browser console (F12) |

---

## 📦 Requirements

```txt
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=2.0.0
Flask>=3.0.0
joblib>=1.3.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
```

---

## 📊 Sample Data Format

**Required columns:** `pol`, `lane`, `container_state`, `cancel`, `broken_route`  
**Optional:** `pod`, `bundle`, `booking_date`, `booking_no`

---

## 🔐 Production Deployment

**Security:** Change `SECRET_KEY`, add authentication, enable HTTPS  
**Performance:** Use gunicorn/uwsgi, Redis caching, PostgreSQL  
**Monitoring:** Add logging, error tracking, model performance monitoring

**Current Deployment:** Hosted on Render at [https://logistic-ml-2.onrender.com](https://logistic-ml-2.onrender.com)

---

## 📝 Key Files

- `app.py` - Flask entry point
- `train_model.py` - Train ML models
- `populate_database.py` - Load data to DB
- `backend/routes_api.py` - API endpoints
- `core/predictor.py` - ML prediction service
- `services/analytics.py` - Dashboard analytics

---

## 📄 License

MIT License

---

**Built with ❤️ for logistics optimization** | *Updated: 2025*

🚀 **Live at:** [https://logistic-ml-2.onrender.com](https://logistic-ml-2.onrender.com)
