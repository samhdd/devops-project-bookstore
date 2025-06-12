#!/usr/bin/env python3
"""
Script to create the PostgreSQL database if it doesn't exist.
Run this before starting the Flask app.
"""
import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'bookstore')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

def create_database():
    """Create the database if it doesn't exist."""
    # Connect to the default PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    try:
        with conn.cursor() as cur:
            # Check if the database exists
            cur.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (DB_NAME,)
            )
            exists = cur.fetchone()
            
            if not exists:
                print(f"Creating database {DB_NAME}...")
                # Create the database
                cur.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_NAME)
                ))
                print(f"Database {DB_NAME} created successfully.")
            else:
                print(f"Database {DB_NAME} already exists.")
                
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
