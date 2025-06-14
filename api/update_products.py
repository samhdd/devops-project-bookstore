#!/usr/bin/env python3
"""
Script to insert the missing products into the database.
"""
import os
import sys
import psycopg2
from main import mock_products

# Database connection configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'bookstore')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

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

def update_products():
    """Check for missing products and add them to the database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Get existing product IDs
            cur.execute('SELECT id FROM products')
            existing_ids = {row[0] for row in cur.fetchall()}
            print(f"Found {len(existing_ids)} existing products: {existing_ids}")
            
            # Show all mock products
            print("All mock products:")
            for p in mock_products:
                print(f"  {p['id']} - {p['name']}")
                
            # Find missing products
            missing_products = [p for p in mock_products if p['id'] not in existing_ids]
            print(f"Found {len(missing_products)} missing products:")
            for p in missing_products:
                print(f"  Missing: {p['id']} - {p['name']}")
            
            # Insert missing products
            for product in missing_products:
                print(f"Adding product: {product['id']} - {product['name']}")
                try:
                    cur.execute('''
                    INSERT INTO products (id, name, author, price, category_id, category, 
                                        description, image_url, pages, published) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        product['id'], 
                        product['name'],
                        product['author'],
                        product['price'],
                        product['categoryId'],
                        product['category'],
                        product['description'],
                        f"/api/images/books/{os.path.basename(product['imageUrl'])}" if product.get('imageUrl') else None,
                        product.get('pages'),
                        product.get('published')
                    ))
                    print(f"  Successfully added {product['id']} - {product['name']}")
                except Exception as e:
                    print(f"  Error adding {product['id']} - {product['name']}: {e}")
            
            conn.commit()
            print("Products updated successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error updating products: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_products()
