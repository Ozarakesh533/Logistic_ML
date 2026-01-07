@echo off
echo ========================================
echo Starting Logistics ML Dashboard
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if models exist
if not exist "artifacts\model_trainer\cancel_model.pkl" (
    echo WARNING: Models not found!
    echo Please run: python train_model.py
    echo.
    pause
)

REM Start Flask app
echo Starting Flask application...
echo.
echo Dashboard will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

