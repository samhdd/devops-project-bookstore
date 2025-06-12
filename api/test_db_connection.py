#!/usr/bin/env python3
"""
Script to test PostgreSQL connectivity and ensure the database is ready.
"""
import os
import sys
import time
import psycopg2
from config import DB_CONFIG

# Maximum number of connection attempts
MAX_ATTEMPTS = 5
WAIT_SECONDS = 3

# Database configuration
DB_HOST = DB_CONFIG['host']
DB_PORT = DB_CONFIG['port']
DB_NAME = DB_CONFIG['database']
DB_USER = DB_CONFIG['user']
DB_PASSWORD = DB_CONFIG['password']

def test_db_connection():
    """Test connection to PostgreSQL database"""
    print(f"Testing connection to PostgreSQL at {DB_HOST}:{DB_PORT}...")
    
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            # Try to connect to the server first (not the specific db)
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database="postgres"
            )
            conn.close()
            print("✅ PostgreSQL server connection successful!")
            
            # Then try the specific database
            try:
                conn = psycopg2.connect(
                    host=DB_HOST,
                    port=DB_PORT,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME
                )
                
                # Perform a simple query to verify everything works
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()[0]
                    if result == 1:
                        print(f"✅ Connection to '{DB_NAME}' database successful!")
                        return True
                conn.close()
            except psycopg2.OperationalError as e:
                if "does not exist" in str(e):
                    print(f"Database '{DB_NAME}' does not exist yet. Will be created.")
                    return True
                raise
            
        except Exception as e:
            attempts += 1
            if attempts < MAX_ATTEMPTS:
                print(f"Connection attempt {attempts} failed: {e}")
                print(f"Retrying in {WAIT_SECONDS} seconds...")
                time.sleep(WAIT_SECONDS)
            else:
                print(f"❌ Failed to connect to PostgreSQL after {MAX_ATTEMPTS} attempts: {e}")
                return False
    
    return False

if __name__ == "__main__":
    if not test_db_connection():
        print("ERROR: Could not connect to PostgreSQL database.")
        sys.exit(1)
    sys.exit(0)
