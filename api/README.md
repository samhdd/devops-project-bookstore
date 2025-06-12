# Bookstore API with PostgreSQL

This API connects to a PostgreSQL database for persistent storage of bookstore data.

## Database Setup

1. Ensure PostgreSQL is installed and running on your system or in a container.

2. Create the database (if it doesn't exist yet):
```bash
python create_db.py
```

3. The Flask application will automatically initialize the database tables when it starts.

## Environment Variables

You can configure the database connection using the following environment variables:

- `DB_HOST`: PostgreSQL server host (default: localhost)
- `DB_PORT`: PostgreSQL server port (default: 5432)
- `DB_NAME`: Database name (default: bookstore)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: postgres)

Example:
```bash
export DB_HOST=postgres-server
export DB_PORT=5432
export DB_NAME=bookstore
export DB_USER=myuser
export DB_PASSWORD=mypassword
```

## Running the API

```bash
python main.py
```

The API will be available at http://localhost:5000

## API Endpoints

- `/api/categories` - Get all book categories
- `/api/categories/<category_id>` - Get a specific category by ID
- `/api/categories/<category_id>/products` - Get all products in a category
- `/api/products/featured` - Get featured products
- `/api/products/<product_id>` - Get a specific product by ID
- `/api/cart` - Get the current shopping cart
- `/api/cart/add` - Add an item to the cart (POST)
- `/api/cart/update` - Update cart item quantity (POST)
- `/api/cart/remove/<item_id>` - Remove an item from the cart (DELETE)
- `/api/cart/checkout` - Check out and clear the cart (POST)
