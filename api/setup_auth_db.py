#!/usr/bin/env python
# Add authentication tables to the database

import psycopg2
from config import DATABASE_CONFIG
import os

def setup_auth_schema():
    """Set up the authentication schema in the database."""
    print("Setting up authentication schema...")
    
    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read the SQL file with auth schema
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'db_auth_schema.sql'), 'r') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        cursor.execute(sql_script)
        
        print("Authentication schema successfully created!")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error setting up authentication schema: {e}")
        return False
    
    return True

if __name__ == "__main__":
    setup_auth_schema()
