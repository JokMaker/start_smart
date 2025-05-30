import os
from pathlib import Path

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-development-only')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + str(Path(__file__).parent / 'startsmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Static Files (optimized)
    STATIC_FOLDER = 'static'
    STATIC_URL_PATH = '/static'
    
    # Cache Control for Static Files (production)
    SEND_FILE_MAX_AGE_DEFAULT = 86400  # 1 day cache for static files