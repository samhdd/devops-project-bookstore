"""
Authentication API endpoints for the bookstore application.
"""

from flask import Blueprint, request, jsonify
from auth import AuthManager, token_required, admin_required
from config import DATABASE_CONFIG

auth_bp = Blueprint('auth', __name__)
auth_manager = AuthManager(DATABASE_CONFIG)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    # Check required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"{field} is required"}), 400
    
    # Get form data
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    
    # Register user
    result = auth_manager.register_user(email, password, first_name, last_name)
    
    if result["success"]:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user and return a JWT token."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    # Check required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"{field} is required"}), 400
    
    # Get form data
    email = data.get('email')
    password = data.get('password')
    
    # Login user
    result = auth_manager.login_user(email, password)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id, user_email, user_role):
    """Get user profile information."""
    try:
        # Connect to database
        import psycopg2
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        # Get user details
        cursor.execute(
            """
            SELECT id, email, first_name, last_name, created_at, last_login, role
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Close connection
        cursor.close()
        conn.close()
        
        # Return user profile
        user_data = {
            "id": user[0],
            "email": user[1],
            "firstName": user[2],
            "lastName": user[3],
            "createdAt": user[4].isoformat() if user[4] else None,
            "lastLogin": user[5].isoformat() if user[5] else None,
            "role": user[6]
        }
        
        return jsonify({
            "success": True,
            "user": user_data
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Error retrieving profile: {str(e)}"}), 500

@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify a JWT token."""
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({"success": False, "message": "Token is required"}), 400
    
    # Verify token
    token = data.get('token')
    result = auth_manager.verify_token(token)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Initiate the password reset process."""
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({"success": False, "message": "Email is required"}), 400
    
    email = data.get('email')
    
    # Create a password reset token
    result = auth_manager.create_password_reset_token(email)
    
    # Always return success even if email doesn't exist (to prevent email enumeration)
    return jsonify(result), 200

@auth_bp.route('/reset-password/<token>', methods=['GET'])
def verify_reset_token(token):
    """Verify if a password reset token is valid."""
    result = auth_manager.verify_reset_token(token)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset a password using a valid token."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    # Check required fields
    required_fields = ['token', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"success": False, "message": f"{field} is required"}), 400
    
    token = data.get('token')
    password = data.get('password')
    
    # Reset password
    result = auth_manager.reset_password(token, password)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400
