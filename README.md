# Bookstore Application

This application consists of a Flask API backend and a React frontend for a bookstore that specializes in Russian literature.

## Features

- Browse books by category
- View featured books on the homepage
- View detailed information about each book
- Add books to cart
- Update cart quantities
- Remove items from cart

## Recent Updates

- PostgreSQL database integration
- Data type handling improvements
- Enhanced image loading with direct database URL usage
- Added API endpoints for image diagnostics and direct image serving
- Removed debugging components from production views

## Directory Structure

- `/api` - Flask API backend
- `/ui` - React frontend

## Running the Application

You can run the application using the start script:

```bash
chmod +x start.sh
./start.sh
```

Or run the components separately:

### Backend (Flask API)

```bash
cd api
python main.py
```

### Frontend (React)

```bash
cd ui
node server.js
```

## API Endpoints

- `/api/categories` - Get all categories
- `/api/categories/:id` - Get a specific category
- `/api/categories/:id/products` - Get products in a category
- `/api/products/:id` - Get a specific product
- `/api/products/featured` - Get featured products
- `/api/cart` - Get cart contents
- `/api/cart/add` - Add item to cart
- `/api/cart/update` - Update cart item quantity
- `/api/cart/remove/:id` - Remove item from cart
- `/api/cart/checkout` - Checkout (clears cart)
- `/api/images/books/:filename` - Serve book images directly
- `/api/debug/images` - Debug image loading issues

## Image Loading

The application now uses a more robust approach for loading book cover images:

1. The API normalizes image URLs before sending them to the frontend
2. The frontend accepts direct image URLs from the database
3. A fallback system ensures images display properly in all scenarios
