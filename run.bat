@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Setting up database...
python db_setup.py

echo Starting StartSmart application...
@echo off
echo Starting StartSmart Application...
echo.
echo Initializing database...
python init_fresh_db.py
echo.
echo Starting Flask server...
python start_app.py
pause