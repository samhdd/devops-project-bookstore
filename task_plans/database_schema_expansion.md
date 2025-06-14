# Database Schema Expansion Plan

## Overview
Expand the current database schema to support user accounts, order processing, and enhanced product management.

## Tasks

### 1. User Management Schema

- [ ] Create users table
  ```sql
  CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
  );
  ```

- [ ] Create user_profiles table
  ```sql
  CREATE TABLE user_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    profile_picture VARCHAR(255),
    phone VARCHAR(20),
    date_of_birth DATE,
    preferences JSONB
  );
  ```

### 2. Order Processing Schema

- [ ] Create orders table
  ```sql
  CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'pending',
    shipping_address_id INTEGER,
    payment_method VARCHAR(50)
  );
  ```

- [ ] Create order_items table
  ```sql
  CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    price DECIMAL(10,2)
  );
  ```

- [ ] Create shipping_addresses table
  ```sql
  CREATE TABLE shipping_addresses (
    address_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    name VARCHAR(100),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    is_default BOOLEAN DEFAULT FALSE
  );
  ```

### 3. Product Enhancements

- [ ] Add fields to products table
  ```sql
  ALTER TABLE products 
    ADD COLUMN stock_quantity INTEGER DEFAULT 0,
    ADD COLUMN publisher VARCHAR(100),
    ADD COLUMN publication_date DATE,
    ADD COLUMN language VARCHAR(50),
    ADD COLUMN dimensions VARCHAR(100),
    ADD COLUMN weight DECIMAL(10,2),
    ADD COLUMN tags JSONB;
  ```

- [ ] Create reviews table
  ```sql
  CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    user_id INTEGER REFERENCES users(user_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified_purchase BOOLEAN DEFAULT FALSE
  );
  ```

### 4. Data Migration

- [ ] Create migration script for adding sample data
- [ ] Update existing product seeding script
- [ ] Create indexes for performance optimization

### 5. API Updates

- [ ] Add new endpoints for user management
- [ ] Add new endpoints for order processing
- [ ] Enhance product endpoints with new fields
- [ ] Add review endpoints

## Estimated Timeline
- Schema design and validation: 1-2 days
- Implementation and SQL scripting: 2-3 days
- Data migration development: 1-2 days
- API integration: 2-3 days

Total: 6-10 days
