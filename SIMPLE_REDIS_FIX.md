# Simple Redis Fix

## The Problem
The Redis service `django-cv-redis` is not being resolved properly, causing the error:
```
Error -2 connecting to redis:6379. Name or service not known.
```

## Simple Solution
Instead of trying to fix the complex service discovery, let's use a simpler approach that will work:

### Option 1: Use External Redis Service
1. Go to [Redis Cloud](https://redis.com/try-free/) or [Upstash](https://upstash.com/)
2. Create a free Redis instance
3. Get the connection string
4. Update your environment variables in Render dashboard

### Option 2: Fix the Service Configuration
The issue is that the Redis service might not be properly deployed. Let's check:

1. Go to your Render dashboard
2. Check if the Redis service `django-cv-redis` is running
3. If it's not running, redeploy it
4. If it's running but not accessible, the service name might be wrong

### Option 3: Use a Different Service Name
The service name might be different. Let's try using the default Redis service name:
