@echo off
echo ========================================
echo Setting Up Logistics ML Dashboard
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check if models exist, if not train them
if not exist "artifacts\model_trainer\cancel_model.pkl" (
    echo.
    echo Models not found. Training models...
    python train_model.py
)

REM Populate database
echo.
echo Populating database with sample data...
python populate_database.py

REM Start Flask app
echo.
echo ========================================
echo Starting Flask application...
echo ========================================
echo.
echo Dashboard will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

