"""
Database configuration file for the Flask API
"""
import os

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'database': os.environ.get('DB_NAME', 'bookstore'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
}

# Additional configuration
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
PORT = int(os.environ.get('PORT', 5000))
