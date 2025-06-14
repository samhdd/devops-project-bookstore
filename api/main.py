# app.py
from flask import Flask, jsonify, request
import os
import sys
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from config import DB_CONFIG, DEBUG, PORT
from auth_routes import auth_bp
from auth import token_required, admin_required

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Register authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Database connection configuration from config.py
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

# For backwards compatibility during transition - original mock data
mock_categories = [
    {"id": "classics", "name": "Classics", "description": "Timeless masterpieces from renowned authors."},
    {"id": "modern", "name": "Modern Literature", "description": "Contemporary works from modern authors."},
    {"id": "poetry", "name": "Poetry", "description": "Beautiful poetry from literary giants."},
    {"id": "fiction", "name": "Fiction", "description": "Fictional works with universal appeal."},
    {"id": "fantasy", "name": "Fantasy", "description": "Magical and fantastical stories."},
    {"id": "science", "name": "Science", "description": "Scientific exploration and discovery."}
]

mock_products = [
    {
        "id": "1", 
        "name": "War and Peace", 
        "author": "Leo Tolstoy",
        "price": 24.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "War and Peace is a novel by Leo Tolstoy, published in 1869. It is regarded as one of Tolstoy's finest literary achievements and remains an internationally praised classic of world literature.",
        "imageUrl": "/images/books/war-and-peace-leo-tolstoy.jpg",
        "pages": 1225,
        "published": 1869
    },
    {
        "id": "2", 
        "name": "Anna Karenina", 
        "author": "Leo Tolstoy",
        "price": 19.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "Anna Karenina is a novel by Leo Tolstoy, first published in book form in 1878. Widely considered a pinnacle in realist fiction, Tolstoy himself called it his first true novel.",
        "imageUrl": "/images/books/anna-karenina-leo-tolstoy.jpg",
        "pages": 864,
        "published": 1878
    },
    {
        "id": "3", 
        "name": "Crime and Punishment", 
        "author": "Fyodor Dostoevsky",
        "price": 18.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "Crime and Punishment focuses on the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg who formulates a plan to kill an unscrupulous pawnbroker for her money.",
        "imageUrl": "/images/books/crime-and-punishment-fyodor-dostoevsky.jpg",
        "pages": 671,
        "published": 1866
    },
    {
        "id": "4", 
        "name": "The Idiot", 
        "author": "Fyodor Dostoevsky",
        "price": 17.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "The Idiot is a novel by Fyodor Dostoevsky. It was first published serially in the journal The Russian Messenger in 1868–69. The title is an ironic reference to the central character of the novel, Prince Lev Nikolayevich Myshkin.",
        "imageUrl": "/images/books/the-idiot-fyodor-dostoevsky.jpg",
        "pages": 652,
        "published": 1869
    },
    {
        "id": "5", 
        "name": "Eugene Onegin", 
        "author": "Alexander Pushkin",
        "price": 15.99, 
        "categoryId": "poetry",
        "category": "Poetry",
        "description": "Eugene Onegin is a novel in verse written by Alexander Pushkin. Onegin is considered a classic of literature, and its eponymous protagonist has served as the model for a number of literary heroes.",
        "imageUrl": "/images/books/eugene-onegin-alexander-pushkin.jpg",
        "pages": 224,
        "published": 1833
    },
    {
        "id": "6", 
        "name": "Fathers and Sons", 
        "author": "Ivan Turgenev",
        "price": 16.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "Fathers and Sons, also translated more literally as Fathers and Children, is an 1862 novel by Ivan Turgenev, published in Moscow by Grachev & Co. It is one of the most acclaimed novels of the 19th century.",
        "imageUrl": "/images/books/fathers-and-sons-ivan-turgenev.jpg",
        "pages": 226,
        "published": 1862
    },
    {
        "id": "7", 
        "name": "The Master and Margarita", 
        "author": "Mikhail Bulgakov",
        "price": 21.99, 
        "categoryId": "modern",
        "category": "Modern Literature",
        "description": "The Master and Margarita is a novel by Mikhail Bulgakov, written between 1928 and 1940 during Stalin's regime. A censored version was published in Moscow magazine in 1966–1967, after the writer's death.",
        "imageUrl": "/images/books/master-and-margarita-mikhail-bulgakov.jpg",
        "pages": 384,
        "published": 1967
    },
    {
        "id": "8", 
        "name": "The Lower Depths", 
        "author": "Maxim Gorky",
        "price": 14.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "The Lower Depths is a play by Maxim Gorky, written in 1902. It was a sensation at the Moscow Art Theatre, and it established Gorky's reputation as one of the leading writers.",
        "imageUrl": "/images/books/the-lower-depths-maxim-gorky.jpg",
        "pages": 115,
        "published": 1902
    },
    {
        "id": "9", 
        "name": "What Dreams May Come", 
        "author": "Richard Matheson",
        "price": 16.99, 
        "categoryId": "modern",
        "category": "Modern",
        "description": "What Dreams May Come is a 1978 novel by Richard Matheson. The plot centers on Chris, a man who dies and goes to Heaven, but descends into Hell to rescue his wife. It was adapted into the 1998 film of the same name.",
        "imageUrl": "/images/books/what-dreams-may-come-richard-matheson.jpg",
        "pages": 288,
        "published": 1978
    },
    {
        "id": "10", 
        "name": "Dracula", 
        "author": "Bram Stoker",
        "price": 14.99, 
        "categoryId": "classics",
        "category": "Classics",
        "description": "Dracula is an 1897 Gothic horror novel by Irish author Bram Stoker. It introduced the character of Count Dracula and established many conventions of subsequent vampire fantasy.",
        "imageUrl": "/images/books/bram-stoker-dracula.jpg",
        "pages": 418,
        "published": 1897
    },
    {
        "id": "14", 
        "name": "Pan's Labyrinth", 
        "author": "Guillermo del Toro",
        "price": 22.99, 
        "categoryId": "fiction",
        "category": "Fiction",
        "description": "Pan's Labyrinth: The Labyrinth of the Faun is a dark fantasy novel written by Guillermo del Toro and Cornelia Funke, based on the acclaimed 2006 film. It takes place in Spain during the summer of 1944 and tells of a young girl who discovers a magical labyrinth.",
        "imageUrl": "/images/books/pan-labyrinth.jpg",
        "pages": 272,
        "published": 2019
    },
    {
        "id": "11", 
        "name": "Harry Potter and the Chamber of Secrets", 
        "author": "J.K. Rowling",
        "price": 18.99, 
        "categoryId": "fiction",
        "category": "Fiction",
        "description": "Harry Potter and the Chamber of Secrets is the second novel in the Harry Potter series, written by J. K. Rowling. The plot follows Harry's second year at Hogwarts School of Witchcraft and Wizardry, during which a series of messages on the walls of the school's corridors warn that the 'Chamber of Secrets' has been opened.",
        "imageUrl": "/images/books/harry-potter-chamber-of-secrets.webp",
        "pages": 352,
        "published": 1998
    },
    {
        "id": "12", 
        "name": "Harry Potter and the Prisoner of Bab El Oued", 
        "author": "J.K. Rowling",
        "price": 19.99, 
        "categoryId": "fiction",
        "category": "Fiction",
        "description": "Harry Potter and the Prisoner of Azkaban is the third novel in the Harry Potter series, written by J. K. Rowling. The book follows Harry Potter, a young wizard, in his third year at Hogwarts School of Witchcraft and Wizardry.",
        "imageUrl": "/images/books/prisoner-of-azkaban.webp",
        "pages": 448,
        "published": 1999
    },
    {
        "id": "13", 
        "name": "Mysteries of the Universe", 
        "author": "Will Gater",
        "price": 27.99, 
        "categoryId": "fiction",
        "category": "Fiction",
        "description": "Mysteries of the Universe explores the wonders of space, featuring stunning images and detailed explanations about galaxies, stars, planets, and cosmic phenomena.",
        "imageUrl": "/images/books/mysteries-of-the-Universe-by-will-gater.jpg",
        "pages": 224,
        "published": 2020
    }
]

# Mock cart data
mock_cart = []

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM categories')
            categories = cur.fetchall()
            return jsonify(categories)
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
            category = cur.fetchone()
            if category:
                return jsonify(category)
            return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/categories/<category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM products WHERE category_id = %s', (category_id,))
            products = cur.fetchall()
            
            # Convert price from Decimal to float for JSON serialization
            for product in products:
                if product['price']:
                    product['price'] = float(product['price'])
            
            # Normalize image URLs
            products = normalize_product_image_urls(products, as_list=True)
            
            return jsonify(products)
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/featured', methods=['GET'])
def get_featured_products():
    # Return a subset of products as featured
    featured_ids = ["1", "3", "7", "11", "8"]
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            placeholders = ', '.join(['%s'] * len(featured_ids))
            cur.execute(f'SELECT * FROM products WHERE id IN ({placeholders})', featured_ids)
            featured = cur.fetchall()
            
            # Convert price from Decimal to float for JSON serialization
            for product in featured:
                if product['price']:
                    product['price'] = float(product['price'])
            
            # Normalize image URLs
            featured = normalize_product_image_urls(featured, as_list=True)
            
            return jsonify(featured)
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product = cur.fetchone()
            if product:
                # Convert price from Decimal to float for JSON serialization
                if product['price']:
                    product['price'] = float(product['price'])
                
                # Normalize image URL
                product = normalize_product_image_urls(product)
                
                return jsonify(product)
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart', methods=['GET'])
def get_cart():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # For simplicity, we're not tracking users, but in a real app
            # you'd filter by user_id
            cur.execute('SELECT * FROM cart_items')
            cart_items = cur.fetchall()
            
            # Convert price from Decimal to float for JSON serialization
            for item in cart_items:
                if item['price']:
                    item['price'] = float(item['price'])
            
            # Normalize image URLs in cart items
            for item in cart_items:
                if item.get('image_url'):
                    item = normalize_product_image_urls(item)
            
            return jsonify(cart_items)
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('productId')
    quantity = data.get('quantity', 1)
    
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get product details
            cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product = cur.fetchone()
            
            if not product:
                return jsonify({"error": "Product not found"}), 404
            
            # Check if the product is already in the cart
            cur.execute('SELECT * FROM cart_items WHERE product_id = %s', (product_id,))
            cart_item = cur.fetchone()
            
            if cart_item:
                # Update quantity
                cur.execute(
                    'UPDATE cart_items SET quantity = quantity + %s WHERE product_id = %s',
                    (quantity, product_id)
                )
            else:
                # Add new item - normalize image URL before storing
                image_url = product['image_url']
                # If there is an image_url, normalize it for consistency
                if image_url:
                    normalized_product = normalize_product_image_urls({'image_url': image_url})
                    image_url = normalized_product['image_url']
                
                cur.execute(
                    '''INSERT INTO cart_items 
                       (product_id, name, author, price, quantity, image_url) 
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (product_id, product['name'], product['author'], product['price'], 
                     quantity, image_url)
                )
            
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.json
    item_id = data.get('itemId')
    quantity = data.get('quantity')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # First check if the item exists
            cur.execute('SELECT * FROM cart_items WHERE product_id = %s', (item_id,))
            if cur.fetchone() is None:
                return jsonify({"error": "Item not found in cart"}), 404
            
            # Update the quantity
            cur.execute('UPDATE cart_items SET quantity = %s WHERE product_id = %s', 
                       (quantity, item_id))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart/remove/<item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM cart_items WHERE product_id = %s', (item_id,))
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # In a real app, we would process payment, create order, etc.
            cur.execute('DELETE FROM cart_items')
            conn.commit()
            return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Function to initialize the database
def init_db():
    """Initialize the database tables if they don't exist"""
    try:
        # First, ensure the database exists
        from create_db import create_database
        create_database()
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Check if tables exist
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'categories'
                    );
                """)
                tables_exist = cur.fetchone()[0]
                
                if not tables_exist:
                    app.logger.info("Tables don't exist. Creating them...")
                    # Read and execute the SQL from db_setup.sql
                    with open('db_setup.sql', 'r') as f:
                        # Split the SQL statements by semicolon
                        sql_statements = f.read().split(';')
                        
                        # Execute each statement
                        for statement in sql_statements:
                            if statement.strip():  # Skip empty statements
                                cur.execute(statement)
                
                conn.commit()
                app.logger.info("Database initialized successfully")
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Error initializing database tables: {e}")
        finally:
            conn.close()
    except Exception as e:
        app.logger.error(f"Error ensuring database exists: {e}")

# New endpoint for debugging image access
@app.route('/api/debug/images', methods=['GET'])
def debug_images():
    """
    Debug endpoint to help troubleshoot image loading issues.
    Returns information about image paths and availability.
    """
    import os
    from flask import send_file
    
    # Base directory for images
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'ui', 'public', 'images', 'books')
    
    # Get all book images
    image_files = []
    if os.path.exists(img_dir):
        image_files = os.listdir(img_dir)
    
    # Get all products and their image paths
    conn = get_db_connection()
    try:
        products_with_images = []
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT id, name, image_url FROM products')
            products = cur.fetchall()
            
            for product in products:
                # Extract just the filename from the path
                if product['image_url']:
                    filename = os.path.basename(product['image_url'])
                    exists = filename in image_files
                else:
                    filename = None
                    exists = False
                
                products_with_images.append({
                    'id': product['id'],
                    'name': product['name'],
                    'image_url': product['image_url'],
                    'filename': filename,
                    'exists': exists
                })
                
        return jsonify({
            'image_dir': img_dir,
            'total_images': len(image_files),
            'image_files': image_files,
            'products': products_with_images
        })
    except Exception as e:
        app.logger.error(f"Error in debug endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Image serving endpoint
@app.route('/api/images/books/<image_filename>', methods=['GET'])
def serve_book_image(image_filename):
    """
    Serve book images directly from the API.
    This can be helpful when the frontend might not have direct access to image files,
    or for tracking image access.
    """
    import os
    from flask import send_from_directory, abort
    
    # Base directory for images - using a consistent location
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'ui', 'public', 'images', 'books')
    
    app.logger.info(f"Request for image: {image_filename}")
    
    try:
        if os.path.exists(os.path.join(img_dir, image_filename)):
            return send_from_directory(img_dir, image_filename)
        else:
            app.logger.error(f"Image not found: {image_filename}")
            abort(404)
    except Exception as e:
        app.logger.error(f"Error serving image {image_filename}: {e}")
        abort(500)

# Catch-all route to handle frontend routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # If the requested path doesn't match any API routes,
    # it's likely a frontend route. Since this is a SPA,
    # we need to return an error for direct access to routes.
    # In production, you'd serve the frontend index.html here.
    if not path.startswith('api/'):
        return jsonify({
            "error": "This endpoint doesn't exist on the server. If you're trying to access a frontend route directly, please navigate from the homepage instead.",
            "path": path
        }), 404
    return jsonify({"error": "Not found"}), 404

def normalize_product_image_urls(product_data, as_list=False):
    """
    Utility function to normalize image URLs in product data.
    This ensures image URLs from the database are properly formatted for frontend use.
    
    Args:
        product_data: A single product dict or a list of products
        as_list: Whether the input is a list of products
        
    Returns:
        The product data with normalized image URLs
    """
    base_url = '/api/images'  # Use the new API endpoint
    
    def normalize_single_product(product):
        if product and 'image_url' in product and product['image_url']:
            # If the URL doesn't already start with our base URL or http
            if not (product['image_url'].startswith(base_url) or 
                    product['image_url'].startswith('http')):
                # Extract the filename from the path
                filename = os.path.basename(product['image_url'])
                # Build the new URL using our API endpoint
                product['image_url'] = f"{base_url}/books/{filename}"
        return product
    
    if as_list:
        return [normalize_single_product(p) for p in product_data]
    else:
        return normalize_single_product(product_data)

if __name__ == '__main__':
    # Initialize the database before starting the app
    init_db()
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)