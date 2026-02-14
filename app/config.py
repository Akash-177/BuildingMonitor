import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the Flask app"""
    
    # Secret key for sessions (security)
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    
    # Database connection string
    # Format: mysql+pymysql://username:password@host/database_name
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/"
        f"{os.getenv('DB_NAME')}"
    )
    
    # Disable modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False