from django.core.management.base import BaseCommand
from django.conf import settings
import redis


class Command(BaseCommand):
    help = 'Test Redis connection for Celery'

    def handle(self, *args, **options):
        self.stdout.write("Testing Redis connection...")
        
        broker_url = settings.CELERY_BROKER_URL
        result_backend = settings.CELERY_RESULT_BACKEND
        
        self.stdout.write(f"Broker URL: {broker_url}")
        self.stdout.write(f"Result Backend: {result_backend}")
        
        try:
            # Test broker connection
            broker_client = redis.from_url(broker_url, socket_connect_timeout=10, socket_timeout=10)
            broker_result = broker_client.ping()
            self.stdout.write(self.style.SUCCESS(f"✅ Broker connection successful: {broker_result}"))
            
            # Test result backend connection
            result_client = redis.from_url(result_backend, socket_connect_timeout=10, socket_timeout=10)
            result_result = result_client.ping()
            self.stdout.write(self.style.SUCCESS(f"✅ Result backend connection successful: {result_result}"))
            
            # Test basic operations
            broker_client.set('test_key', 'test_value', ex=60)
            value = broker_client.get('test_key')
            self.stdout.write(self.style.SUCCESS(f"✅ Redis operations test successful: {value.decode() if value else 'None'}"))
            
            # Clean up
            broker_client.delete('test_key')
            
            self.stdout.write(self.style.SUCCESS("🎉 All Redis tests passed!"))
            
        except redis.ConnectionError as e:
            self.stdout.write(self.style.ERROR(f"❌ Redis connection failed: {e}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {e}"))
            return
