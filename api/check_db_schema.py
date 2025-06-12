#!/usr/bin/env python3
"""
Script to check and update the database schema to ensure image_url fields exist.
"""
import os
import sys
import psycopg2
from psycopg2 import sql
from config import DB_CONFIG

# Database configuration
DB_HOST = DB_CONFIG['host']
DB_PORT = DB_CONFIG['port'] 
DB_NAME = DB_CONFIG['database']
DB_USER = DB_CONFIG['user']
DB_PASSWORD = DB_CONFIG['password']

def get_db_connection():
    """Create a database connection and return it"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.autocommit = False
    return conn

def check_image_url_columns():
    """Check if image_url columns exist in products and cart_items tables, add them if missing."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Check products table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='products' AND column_name='image_url'
            """)
            if not cur.fetchone():
                print("Adding image_url column to products table")
                cur.execute("""
                    ALTER TABLE products 
                    ADD COLUMN image_url VARCHAR(255)
                """)
            
            # Check cart_items table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='cart_items' AND column_name='image_url'
            """)
            if not cur.fetchone():
                print("Adding image_url column to cart_items table")
                cur.execute("""
                    ALTER TABLE cart_items 
                    ADD COLUMN image_url VARCHAR(255)
                """)
            
            # Update existing products to ensure image_url is properly set
            cur.execute("""
                UPDATE products SET image_url = '/api/images/books/book-' || id || '.jpg'
                WHERE image_url IS NULL OR image_url = ''
            """)
            
            conn.commit()
            print("Database schema checked and updated if needed")
    except Exception as e:
        print(f"Error checking database schema: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    check_image_url_columns()
