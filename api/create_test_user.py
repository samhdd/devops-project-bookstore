#!/usr/bin/env python3
"""Create a test user for development purposes"""

from auth import AuthManager
from config import DATABASE_CONFIG

def create_test_user():
    """Create a test user with admin privileges"""
    print("Creating test user...")
    
    auth_manager = AuthManager(DATABASE_CONFIG)
    
    # Create a regular user
    result = auth_manager.register_user(
        email="user@gmail.com",
        password="Password123",
        first_name="Test",
        last_name="User"
    )
    
    if result["success"]:
        print("✅ Test user created successfully:")
        print("   Email: user@gmail.com")
        print("   Password: Password123")
    else:
        print(f"❌ Failed to create test user: {result['message']}")
    
    # Create an admin user
    import psycopg2
    conn = None
    try:
        # First create regular user
        admin_result = auth_manager.register_user(
            email="admin@gmail.com",
            password="AdminPass123",
            first_name="Admin",
            last_name="User"
        )
        
        if not admin_result["success"]:
            if "already registered" not in admin_result["message"]:
                print(f"❌ Failed to create admin user: {admin_result['message']}")
                return
        
        # Then promote to admin
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET role = 'admin' WHERE email = %s",
            ("admin@gmail.com",)
        )
        conn.commit()
        print("✅ Admin user created successfully:")
        print("   Email: admin@gmail.com")
        print("   Password: AdminPass123")
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_test_user()
