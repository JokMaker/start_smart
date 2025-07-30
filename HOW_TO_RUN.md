# How to Run StartSmart

## Quick Start (Windows)

1. Double-click on `run.bat` file
2. Wait for the application to start
3. Open your browser and go to: http://localhost:5000

## Manual Setup

### 1. Install Dependencies
```
pip install -r requirements.txt
```

### 2. Initialize Database
```
python db_setup.py
```

### 3. Run the Application
```
python run.py
```

### 4. Access the Website
Open your browser and navigate to:
```
http://localhost:5000
```

## Troubleshooting

### Database Issues
If you encounter database issues, try:
```
python db_setup.py
```

### Login/Register Issues
- Make sure the database is properly initialized
- Try with these credentials:
  - Email: admin@startsmart.com
  - Password: admin123

### Job Page Issues
- Make sure you're logged in to apply for jobs
- Only students can apply for jobs
- Only recruiters can post jobs

## Contact

For support, contact:
- Email: j.kur@alustudent.com
- Phone: +250 793 224 036