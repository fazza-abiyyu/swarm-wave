#!/usr/bin/env python3
"""
Health Check Test Script for Swarm Lab Backend
Usage: python3 test_health.py [URL]
"""

import requests
import json
import sys
import time

def test_health_endpoint(base_url="http://localhost:5001"):
    """Test both health endpoints"""
    
    print(f"Testing health endpoints at {base_url}")
    print("=" * 50)
    
    # Test simple health check
    try:
        print("\n🔍 Testing Simple Health Check...")
        response = requests.get(f"{base_url}/health/simple", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simple Health Check: {data['status'].upper()}")
            print(f"⏰ Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Simple Health Check Failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Simple Health Check Error: {e}")
    
    # Test detailed health check
    try:
        print("\n🔍 Testing Detailed Health Check...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Overall Status: {data['status'].upper()}")
            print(f"🏆 Health Score: {data['health_score']}/100")
            print(f"⏱️ Uptime: {data['uptime_seconds']} seconds")
            print(f"🐍 Python Version: {data['system']['python_version']}")
            print(f"💻 Platform: {data['system']['platform']}")
            
            print(f"\n🤖 Algorithms Status:")
            for algo, status in data['algorithms'].items():
                status_icon = "✅" if status['available'] else "❌"
                print(f"  {status_icon} {algo}: {status.get('status', 'unavailable')}")
            
            print(f"\n🔗 Available Endpoints:")
            for name, endpoint in data['endpoints'].items():
                print(f"  • {name}: {endpoint}")
                
        else:
            print(f"❌ Detailed Health Check Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Detailed Health Check Error: {e}")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5001"
    test_health_endpoint(base_url)
