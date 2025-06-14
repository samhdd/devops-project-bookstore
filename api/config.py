"""
Configuration file for the Flask API
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'database': os.environ.get('DB_NAME', 'bookstore'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
}

# Create a standardized config for auth module
DATABASE_CONFIG = DB_CONFIG

# JWT configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'development_secret_key_change_in_production')
JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))

# Additional configuration
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.environ.get('PORT', 5000))
