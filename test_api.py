#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints work
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_api():
    """Test basic API functionality"""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Hoodie Store API...")
        
        # Test health check
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"✅ Health check: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test root endpoint
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Root endpoint failed: {e}")
        
        # Test products endpoint
        try:
            response = await client.get(f"{BASE_URL}/api/v1/products")
            print(f"✅ Products endpoint: {response.status_code}")
            if response.status_code == 200:
                products = response.json()
                print(f"   Found {len(products)} products")
                if products:
                    print(f"   First product: {products[0]['name']}")
        except Exception as e:
            print(f"❌ Products endpoint failed: {e}")
        
        # Test API documentation
        try:
            response = await client.get(f"{BASE_URL}/docs")
            print(f"✅ API docs: {response.status_code}")
        except Exception as e:
            print(f"❌ API docs failed: {e}")
        
        print("\n🎉 API testing completed!")

if __name__ == "__main__":
    asyncio.run(test_api())
