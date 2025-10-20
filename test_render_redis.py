#!/usr/bin/env python3
"""
Test script to identify the correct Redis connection for Render deployment
"""
import os
import socket
import redis

def test_redis_connection():
    print("=== Render Redis Connection Test ===")
    
    # Print all environment variables
    print("\n=== Environment Variables ===")
    for key, value in os.environ.items():
        if 'redis' in key.lower() or 'celery' in key.lower():
            print(f"{key} = {value}")
    
    # Test different Redis hostnames
    redis_hosts = [
        'django-cv-redis',
        'redis',
        'localhost',
        '127.0.0.1'
    ]
    
    print(f"\n=== Testing Redis Hostnames ===")
    for host in redis_hosts:
        print(f"Testing host: {host}")
        try:
            # Test if host is resolvable
            socket.gethostbyname(host)
            print(f"  ✅ Host {host} is resolvable")
            
            # Test Redis connection
            redis_url = f'redis://{host}:6379/0'
            client = redis.from_url(redis_url, socket_connect_timeout=5, socket_timeout=5)
            client.ping()
            print(f"  ✅ Redis connection successful: {redis_url}")
            return redis_url
            
        except socket.gaierror as e:
            print(f"  ❌ Host {host} not resolvable: {e}")
        except redis.ConnectionError as e:
            print(f"  ❌ Redis connection failed for {host}: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error for {host}: {e}")
    
    print("\n❌ No working Redis connection found")
    return None

if __name__ == "__main__":
    result = test_redis_connection()
    if result:
        print(f"\n✅ Working Redis URL: {result}")
    else:
        print(f"\n❌ No working Redis connection found")
