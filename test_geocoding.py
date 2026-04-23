#!/usr/bin/env python3
"""Test geocoding endpoint directly"""
import httpx
import asyncio

async def test_geocode():
    print("Testing geocoding endpoint...")
    print("-" * 50)
    
    # Test 1: Health check
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get('http://127.0.0.1:8001/health', timeout=5.0)
            print(f"✅ Health check: {resp.status_code}")
            print(f"   Response: {resp.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    print()
    
    # Test 2: Geocode suggest
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'http://127.0.0.1:8001/api/geocode/suggest',
                params={'q': 'mumbai'},
                timeout=15.0
            )
            print(f"✅ Geocode suggest: {resp.status_code}")
            data = resp.json()
            print(f"   Found {len(data)} suggestions")
            if data:
                print(f"   First result: {data[0].get('display_name', 'N/A')}")
    except Exception as e:
        print(f"❌ Geocode suggest failed: {e}")
    
    print()
    
    # Test 3: Geocode full address
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'http://127.0.0.1:8001/api/geocode',
                params={'address': 'Mumbai, Maharashtra, India'},
                timeout=15.0
            )
            print(f"✅ Geocode address: {resp.status_code}")
            data = resp.json()
            print(f"   Result: {data}")
    except Exception as e:
        print(f"❌ Geocode address failed: {e}")

if __name__ == '__main__':
    asyncio.run(test_geocode())
