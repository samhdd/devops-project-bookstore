"""
Authentication module for the bookstore API.
Provides user registration, login, and token validation functionality.
"""

import jwt
import datetime
from passlib.hash import bcrypt
from email_validator import validate_email, EmailNotValidError
import re
import psycopg2
from functools import wraps
from flask import request, jsonify, current_app
import os

# JWT Configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'development-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def get_db_connection(config):
    """Create a database connection."""
    return psycopg2.connect(**config)

class AuthManager:
    """Authentication manager for user authentication operations."""
    
    def __init__(self, db_config):
        self.db_config = db_config
    
    def _validate_password(self, password):
        """
        Validate password strength.
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        """
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
            
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
            
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit"
            
        return True, "Password is valid"
    
    def _validate_email(self, email):
        """Validate email format."""
        try:
            valid = validate_email(email)
            return True, "Email is valid"
        except EmailNotValidError as e:
            return False, str(e)
    
    def register_user(self, email, password, first_name, last_name):
        """Register a new user."""
        # Validate email
        is_valid_email, email_msg = self._validate_email(email)
        if not is_valid_email:
            return {"success": False, "message": email_msg}
        
        # Validate password
        is_valid_password, password_msg = self._validate_password(password)
        if not is_valid_password:
            return {"success": False, "message": password_msg}
        
        # Hash the password
        password_hash = bcrypt.hash(password)
        
        # Save to database
        conn = None
        try:
            conn = get_db_connection(self.db_config)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return {"success": False, "message": "Email already registered"}
            
            # Insert new user
            cursor.execute(
                """
                INSERT INTO users (email, password_hash, first_name, last_name) 
                VALUES (%s, %s, %s, %s) RETURNING id
                """,
                (email, password_hash, first_name, last_name)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            return {"success": False, "message": f"Registration error: {str(e)}"}
            
        finally:
            if conn:
                conn.close()
    
    def login_user(self, email, password):
        """Authenticate a user and return a JWT token."""
        conn = None
        try:
            conn = get_db_connection(self.db_config)
            cursor = conn.cursor()
            
            # Get user by email
            cursor.execute(
                "SELECT id, email, password_hash, role FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
            
            if not user:
                return {"success": False, "message": "Invalid email or password"}
            
            user_id, user_email, stored_hash, role = user
            
            # Verify password
            if not bcrypt.verify(password, stored_hash):
                return {"success": False, "message": "Invalid email or password"}
            
            # Generate JWT token
            payload = {
                'sub': user_id,
                'email': user_email,
                'role': role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            
            # Update last login time
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                (user_id,)
            )
            conn.commit()
            
            return {
                "success": True,
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user_id,
                    "email": user_email,
                    "role": role
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}
            
        finally:
            if conn:
                conn.close()
    
    def verify_token(self, token):
        """Verify a JWT token and return user information."""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return {"success": True, "user_id": payload['sub'], "email": payload['email'], "role": payload['role']}
        except jwt.ExpiredSignatureError:
            return {"success": False, "message": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"success": False, "message": "Invalid token"}
    
    def create_password_reset_token(self, email):
        """Create a password reset token for the user."""
        conn = None
        try:
            conn = get_db_connection(self.db_config)
            cursor = conn.cursor()
            
            # Get user by email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                # Don't expose whether the email exists or not to prevent enumeration attacks
                return {"success": True, "message": "If your email is registered, you'll receive a password reset link"}
                
            user_id = user[0]
            
            # Generate a secure token
            import secrets
            import string
            token_chars = string.ascii_letters + string.digits
            token = ''.join(secrets.choice(token_chars) for _ in range(64))
            
            # Set expiration time (24 hours from now)
            expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            
            # Delete any existing password reset tokens for this user
            cursor.execute(
                "DELETE FROM user_tokens WHERE user_id = %s AND token_type = 'password_reset'",
                (user_id,)
            )
            
            # Insert new token
            cursor.execute(
                """
                INSERT INTO user_tokens (user_id, token, token_type, expires_at) 
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, token, 'password_reset', expires_at)
            )
            
            conn.commit()
            
            # In a real application, you would send an email with the reset link
            # For development purposes, we'll just return the token
            return {
                "success": True, 
                "message": "Password reset link has been sent",
                "debug_token": token  # Remove this in production
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            return {"success": False, "message": f"Error creating reset token: {str(e)}"}
            
        finally:
            if conn:
                conn.close()
                
    def verify_reset_token(self, token):
        """Verify if a password reset token is valid."""
        conn = None
        try:
            conn = get_db_connection(self.db_config)
            cursor = conn.cursor()
            
            # Check if token exists and is not expired
            cursor.execute(
                """
                SELECT user_id, expires_at 
                FROM user_tokens 
                WHERE token = %s AND token_type = 'password_reset'
                """,
                (token,)
            )
            
            result = cursor.fetchone()
            
            if not result:
                return {"success": False, "message": "Invalid or expired token"}
                
            user_id, expires_at = result
            
            if datetime.datetime.utcnow() > expires_at:
                return {"success": False, "message": "Token has expired"}
                
            return {"success": True, "user_id": user_id}
            
        except Exception as e:
            return {"success": False, "message": f"Error verifying token: {str(e)}"}
            
        finally:
            if conn:
                conn.close()
                
    def reset_password(self, token, new_password):
        """Reset a user's password using a valid reset token."""
        # Validate password
        is_valid_password, password_msg = self._validate_password(new_password)
        if not is_valid_password:
            return {"success": False, "message": password_msg}
            
        # Verify token
        token_result = self.verify_reset_token(token)
        if not token_result["success"]:
            return token_result
            
        user_id = token_result["user_id"]
        conn = None
        
        try:
            conn = get_db_connection(self.db_config)
            cursor = conn.cursor()
            
            # Hash the new password
            password_hash = bcrypt.hash(new_password)
            
            # Update user's password
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (password_hash, user_id)
            )
            
            # Delete the used token
            cursor.execute(
                "DELETE FROM user_tokens WHERE user_id = %s AND token_type = 'password_reset'",
                (user_id,)
            )
            
            conn.commit()
            
            return {"success": True, "message": "Password has been reset successfully"}
            
        except Exception as e:
            if conn:
                conn.rollback()
            return {"success": False, "message": f"Error resetting password: {str(e)}"}
            
        finally:
            if conn:
                conn.close()
    

def token_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"success": False, "message": "Authentication token is missing"}), 401
        
        # Verify token
        from config import DATABASE_CONFIG
        auth_manager = AuthManager(DATABASE_CONFIG)
        result = auth_manager.verify_token(token)
        
        if not result["success"]:
            return jsonify({"success": False, "message": result["message"]}), 401
        
        # Add user info to kwargs
        kwargs['user_id'] = result["user_id"]
        kwargs['user_email'] = result["email"]
        kwargs['user_role'] = result["role"]
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """Decorator to protect routes that require admin privileges."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"success": False, "message": "Authentication token is missing"}), 401
        
        # Verify token
        from config import DATABASE_CONFIG
        auth_manager = AuthManager(DATABASE_CONFIG)
        result = auth_manager.verify_token(token)
        
        if not result["success"]:
            return jsonify({"success": False, "message": result["message"]}), 401
        
        # Check if user is admin
        if result["role"] != "admin":
            return jsonify({"success": False, "message": "Admin privileges required"}), 403
        
        # Add user info to kwargs
        kwargs['user_id'] = result["user_id"]
        kwargs['user_email'] = result["email"]
        
        return f(*args, **kwargs)
    
    return decorated
