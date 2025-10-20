# Redis Connection Troubleshooting Guide

## Current Issue Analysis

Based on the deployment logs, the issue is that the Redis service `django-cv-redis` is not being resolved properly. The logs show:

1. ✅ Environment variables are being set correctly in `render.yaml`
2. ✅ The fallback logic is detecting the Render environment
3. ✅ The URLs are being updated to use `django-cv-redis:6379/0`
4. ❌ But the Redis service `django-cv-redis` cannot be resolved

## Root Cause

The issue is likely one of the following:

1. **Redis service not deployed**: The Redis service might not be properly deployed or started
2. **Service name mismatch**: The service name in `render.yaml` might not match the actual deployed service
3. **Network connectivity**: There might be a networking issue between services
4. **Render service discovery**: Render's internal service discovery might not be working properly

## Solutions Applied

### 1. Fixed `render.yaml` Configuration
- Changed from hardcoded Redis URLs to using `fromService` syntax
- This should automatically get the correct Redis connection string from Render

### 2. Enhanced Settings with Fallback Logic
- Added comprehensive Redis connection testing
- Added multiple fallback URLs to try
- Added better error handling and debugging

### 3. Added Alternative Connection Methods
- The app will now try multiple Redis URLs if the primary one fails
- Includes fallback to localhost and other common Redis configurations

## Next Steps to Resolve

### Option 1: Check Render Dashboard
1. Go to your Render dashboard
2. Check if the Redis service `django-cv-redis` is deployed and running
3. Verify the service name matches exactly
4. Check if there are any error logs for the Redis service

### Option 2: Verify Service Names
The Redis service name in `render.yaml` must match exactly with what's deployed in Render. Check:
- Service name: `django-cv-redis`
- Service type: `redis`
- Service status: `running`

### Option 3: Test with Different Service Name
If the service name is different, update the `render.yaml` file with the correct name.

### Option 4: Use External Redis Service
If the internal Redis service is not working, you could:
1. Use an external Redis service (like Redis Cloud)
2. Update the environment variables to point to the external service

## Testing the Fix

After deploying the updated configuration:

1. **Check the logs** for the debug messages:
   ```
   DEBUG: Detected Render deployment environment
   DEBUG: Using REDIS_URL from environment: redis://...
   DEBUG: Redis connection test successful
   ```

2. **Test Celery functionality** by using the `/add/` endpoint

3. **Monitor for errors** in the application logs

## Expected Behavior After Fix

1. **Startup logs should show**:
   ```
   DEBUG: Redis connection test successful
   ```

2. **No more Redis connection errors** in the logs

3. **Celery tasks should work** without connection issues

## If the Issue Persists

If the Redis connection still fails after these changes:

1. **Check Render service status** in the dashboard
2. **Verify service names** match exactly
3. **Consider using an external Redis service** as a temporary workaround
4. **Contact Render support** if the internal service discovery is not working

## Files Modified
- `render.yaml` - Updated to use `fromService` syntax for Redis configuration
- `async_demo/settings_production.py` - Enhanced with comprehensive fallback logic

The updated configuration should resolve the Redis connection issues by using Render's proper service discovery mechanism.
