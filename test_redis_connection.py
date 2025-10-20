#!/usr/bin/env python3
"""
Test Redis connection script to debug connection issues
"""
import os
import sys
import redis
from urllib.parse import urlparse

def test_redis_connection():
    print("=== Redis Connection Test ===")
    
    # Get environment variables
    broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    print(f"CELERY_BROKER_URL: {broker_url}")
    print(f"CELERY_RESULT_BACKEND: {result_backend}")
    
    # Parse URLs
    broker_parsed = urlparse(broker_url)
    result_parsed = urlparse(result_backend)
    
    print(f"\nBroker URL parsed:")
    print(f"  Scheme: {broker_parsed.scheme}")
    print(f"  Hostname: {broker_parsed.hostname}")
    print(f"  Port: {broker_parsed.port}")
    print(f"  Path: {broker_parsed.path}")
    
    print(f"\nResult Backend URL parsed:")
    print(f"  Scheme: {result_parsed.scheme}")
    print(f"  Hostname: {result_parsed.hostname}")
    print(f"  Port: {result_parsed.port}")
    print(f"  Path: {result_parsed.path}")
    
    # Test connection
    print(f"\n=== Testing Connection ===")
    try:
        client = redis.from_url(broker_url, socket_connect_timeout=10, socket_timeout=10)
        result = client.ping()
        print(f"✅ Redis connection successful: {result}")
        
        # Test basic operations
        client.set('test_key', 'test_value', ex=60)
        value = client.get('test_key')
        print(f"✅ Redis set/get test successful: {value.decode()}")
        
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("✅ All Redis tests passed!")
    return True

if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)
