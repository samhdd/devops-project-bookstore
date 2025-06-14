#!/usr/bin/env python
# Test script for authentication system

import requests
import json
import time

BASE_URL = 'http://localhost:5000/api/auth'

def print_header(message):
    print("\n" + "-" * 50)
    print(f" {message}")
    print("-" * 50)

def test_register():
    print_header("Testing User Registration")
    
    # Test case 1: Valid registration
    test_user = {
        'email': f'test_user_{int(time.time())}@gmail.com',  # Use timestamp to ensure unique email
        'password': 'TestPassword123',
        'firstName': 'Test',
        'lastName': 'User'
    }
    
    response = requests.post(f'{BASE_URL}/register', json=test_user)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 201, "Registration should return 201 Created status code"
    assert data['success'], "Registration should be successful"
    
    # Keep the test user email for subsequent tests
    return test_user

def test_login(test_user):
    print_header("Testing User Login")
    
    # Valid login
    login_data = {
        'email': test_user['email'],
        'password': test_user['password']
    }
    
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Login should return 200 OK status code"
    assert data['success'], "Login should be successful"
    assert 'token' in data, "Login response should contain a token"
    
    return data['token']

def test_profile(token):
    print_header("Testing Profile Endpoint")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/profile', headers=headers)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Profile should return 200 OK status code"
    assert data['success'], "Profile retrieval should be successful"

def test_forgot_password(test_user):
    print_header("Testing Forgot Password Endpoint")
    
    forgot_data = {
        'email': test_user['email']
    }
    
    response = requests.post(f'{BASE_URL}/forgot-password', json=forgot_data)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Forgot password should return 200 OK status code"
    assert data['success'], "Forgot password should be successful"
    
    # For testing purposes, we should have the debug_token in the response
    assert 'debug_token' in data, "Response should contain debug_token for testing purposes"
    
    return data['debug_token']

def test_reset_password(token, test_user):
    print_header("Testing Reset Password Endpoint")
    
    # First, verify the token
    response = requests.get(f'{BASE_URL}/reset-password/{token}')
    data = response.json()
    
    print(f"Token verification - Status: {response.status_code}")
    print(f"Token verification - Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Token verification should return 200 OK status code"
    assert data['success'], "Token should be valid"
    
    # Now reset the password
    new_password = 'NewTestPass456'
    reset_data = {
        'token': token,
        'password': new_password
    }
    
    response = requests.post(f'{BASE_URL}/reset-password', json=reset_data)
    data = response.json()
    
    print(f"Password reset - Status: {response.status_code}")
    print(f"Password reset - Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Password reset should return 200 OK status code"
    assert data['success'], "Password reset should be successful"
    
    # Update the test user with the new password
    test_user['password'] = new_password
    
    # Try logging in with the new password
    print_header("Testing Login after Password Reset")
    login_data = {
        'email': test_user['email'],
        'password': new_password
    }
    
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200, "Login with new password should return 200 OK status code"
    assert data['success'], "Login with new password should be successful"

if __name__ == "__main__":
    try:
        test_user = test_register()
        token = test_login(test_user)
        test_profile(token)
        reset_token = test_forgot_password(test_user)
        test_reset_password(reset_token, test_user)
        print_header("All Tests Passed!")
    except AssertionError as e:
        print(f"\n❌ Test Failed: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
