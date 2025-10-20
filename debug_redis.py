#!/usr/bin/env python3
"""
Debug Redis connection issues
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_demo.settings_production')

# Setup Django
django.setup()

from django.conf import settings
import redis

def debug_redis_config():
    print("=== Redis Configuration Debug ===")
    print(f"Django Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Allowed Hosts: {settings.ALLOWED_HOSTS}")
    
    print(f"\n=== Celery Configuration ===")
    print(f"CELERY_BROKER_URL: {settings.CELERY_BROKER_URL}")
    print(f"CELERY_RESULT_BACKEND: {settings.CELERY_RESULT_BACKEND}")
    
    print(f"\n=== Environment Variables ===")
    redis_env_vars = {k: v for k, v in os.environ.items() if 'redis' in k.lower() or 'celery' in k.lower()}
    for key, value in redis_env_vars.items():
        print(f"{key}: {value}")
    
    print(f"\n=== Testing Redis Connection ===")
    try:
        client = redis.from_url(settings.CELERY_BROKER_URL, socket_connect_timeout=10, socket_timeout=10)
        result = client.ping()
        print(f"✅ Redis connection successful: {result}")
        
        # Test basic operations
        client.set('debug_test_key', 'debug_test_value', ex=60)
        value = client.get('debug_test_key')
        print(f"✅ Redis set/get test successful: {value.decode()}")
        
        # Clean up
        client.delete('debug_test_key')
        
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        print(f"   Trying to connect to: {settings.CELERY_BROKER_URL}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("✅ All Redis tests passed!")
    return True

if __name__ == "__main__":
    success = debug_redis_config()
    sys.exit(0 if success else 1)
