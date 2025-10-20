from django.core.management.base import BaseCommand
from django.conf import settings
import redis
import socket
import os


class Command(BaseCommand):
    help = 'Test Redis connection for Celery'

    def handle(self, *args, **options):
        self.stdout.write("Testing Redis connection...")
        
        # Print environment variables
        self.stdout.write("\n=== Environment Variables ===")
        for key, value in os.environ.items():
            if 'redis' in key.lower() or 'celery' in key.lower():
                self.stdout.write(f"{key} = {value}")
        
        broker_url = settings.CELERY_BROKER_URL
        result_backend = settings.CELERY_RESULT_BACKEND
        
        self.stdout.write(f"\nBroker URL: {broker_url}")
        self.stdout.write(f"Result Backend: {result_backend}")
        
        # Test different Redis hostnames
        redis_hosts = ['django-cv-redis', 'redis', 'localhost', '127.0.0.1']
        
        self.stdout.write(f"\n=== Testing Redis Hostnames ===")
        working_url = None
        
        for host in redis_hosts:
            self.stdout.write(f"Testing host: {host}")
            try:
                # Test if host is resolvable
                socket.gethostbyname(host)
                self.stdout.write(f"  ✅ Host {host} is resolvable")
                
                # Test Redis connection
                test_url = f'redis://{host}:6379/0'
                client = redis.from_url(test_url, socket_connect_timeout=5, socket_timeout=5)
                client.ping()
                self.stdout.write(f"  ✅ Redis connection successful: {test_url}")
                working_url = test_url
                break
                
            except socket.gaierror as e:
                self.stdout.write(f"  ❌ Host {host} not resolvable: {e}")
            except redis.ConnectionError as e:
                self.stdout.write(f"  ❌ Redis connection failed for {host}: {e}")
            except Exception as e:
                self.stdout.write(f"  ❌ Unexpected error for {host}: {e}")
        
        if working_url:
            self.stdout.write(f"\n✅ Working Redis URL found: {working_url}")
            
            # Test the current configuration
            try:
                broker_client = redis.from_url(broker_url, socket_connect_timeout=10, socket_timeout=10)
                broker_result = broker_client.ping()
                self.stdout.write(self.style.SUCCESS(f"✅ Current broker connection successful: {broker_result}"))
                
                # Test basic operations
                broker_client.set('test_key', 'test_value', ex=60)
                value = broker_client.get('test_key')
                self.stdout.write(self.style.SUCCESS(f"✅ Redis operations test successful: {value.decode() if value else 'None'}"))
                
                # Clean up
                broker_client.delete('test_key')
                
                self.stdout.write(self.style.SUCCESS("🎉 All Redis tests passed!"))
                
            except redis.ConnectionError as e:
                self.stdout.write(self.style.ERROR(f"❌ Current Redis configuration failed: {e}"))
                self.stdout.write(self.style.WARNING(f"💡 Try using: {working_url}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {e}"))
        else:
            self.stdout.write(self.style.ERROR("❌ No working Redis connection found"))
