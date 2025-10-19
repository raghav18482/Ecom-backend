#!/usr/bin/env python3
"""
Test script to debug login endpoint issues
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_login():
    """Test login endpoint specifically"""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Login Endpoint...")
        
        # Test login with invalid credentials first
        try:
            login_data = {
                "email": "test@example.com",
                "password": "wrongpassword"
            }
            response = await client.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            print(f"❌ Login with invalid credentials: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Login test failed: {e}")
        
        # Test login with valid credentials (if user exists)
        try:
            login_data = {
                "email": "test@example.com",
                "password": "testpassword123"
            }
            response = await client.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            print(f"✅ Login with valid credentials: {response.status_code}")
            if response.status_code == 200:
                print(f"   Token: {response.json()}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Login test failed: {e}")
        
        # Test registration first
        try:
            register_data = {
                "email": "test@example.com",
                "password": "testpassword123",
                "full_name": "Test User"
            }
            response = await client.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
            print(f"✅ Registration: {response.status_code}")
            if response.status_code == 201:
                print(f"   User created: {response.json()}")
            else:
                print(f"   Registration error: {response.text}")
        except Exception as e:
            print(f"❌ Registration test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_login())




