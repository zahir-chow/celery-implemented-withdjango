import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# Add common Render domains and localhost
ALLOWED_HOSTS.extend([
    'celery-implemented-withdjango.onrender.com',
    'localhost',
    '127.0.0.1',
])
# Remove empty strings and duplicates
ALLOWED_HOSTS = list(set([host.strip() for host in ALLOWED_HOSTS if host.strip()]))
print(f"DEBUG: ALLOWED_HOSTS = {ALLOWED_HOSTS}")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasksapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'async_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'async_demo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.strip():
    try:
        DATABASES = {
            'default': dj_database_url.parse(
                DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except Exception as e:
        # Fallback to SQLite if DATABASE_URL parsing fails
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Fallback to SQLite if DATABASE_URL is not provided
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Celery configuration
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Add connection timeout and retry settings
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_TASK_TIME_LIMIT = 120

# Redis connection settings for better reliability
CELERY_BROKER_CONNECTION_TIMEOUT = 30
CELERY_RESULT_BACKEND_CONNECTION_TIMEOUT = 30
CELERY_BROKER_HEARTBEAT = 30
CELERY_BROKER_POOL_LIMIT = 10

# Additional Redis configuration with comprehensive fallback logic
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Debug: Print all environment variables that might affect Redis
print(f"DEBUG: All environment variables:")
for key, value in os.environ.items():
    if 'redis' in key.lower() or 'celery' in key.lower():
        print(f"  {key} = {value}")

# Handle different deployment scenarios
if os.environ.get('RENDER') or 'onrender.com' in os.environ.get('ALLOWED_HOSTS', ''):
    # On Render, use the correct Redis service name
    print("DEBUG: Detected Render deployment environment")
    if 'redis://redis:' in CELERY_BROKER_URL:
        CELERY_BROKER_URL = CELERY_BROKER_URL.replace('redis://redis:', 'redis://django-cv-redis:')
        print(f"DEBUG: Updated CELERY_BROKER_URL to: {CELERY_BROKER_URL}")
    if 'redis://redis:' in CELERY_RESULT_BACKEND:
        CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND.replace('redis://redis:', 'redis://django-cv-redis:')
        print(f"DEBUG: Updated CELERY_RESULT_BACKEND to: {CELERY_RESULT_BACKEND}")
    
    # Also try to get Redis URL from Render's internal service discovery
    if 'REDIS_URL' in os.environ:
        redis_url = os.environ['REDIS_URL']
        if redis_url and redis_url.startswith('redis://'):
            CELERY_BROKER_URL = redis_url
            CELERY_RESULT_BACKEND = redis_url
            print(f"DEBUG: Using REDIS_URL from environment: {redis_url}")

# Force Redis to use the same URL for both broker and result backend
if CELERY_BROKER_URL != CELERY_RESULT_BACKEND:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Debug Redis connection
print(f"DEBUG: CELERY_BROKER_URL = {CELERY_BROKER_URL}")
print(f"DEBUG: CELERY_RESULT_BACKEND = {CELERY_RESULT_BACKEND}")

# Test Redis connection on startup
try:
    import redis
    redis_client = redis.from_url(CELERY_BROKER_URL, socket_connect_timeout=5, socket_timeout=5)
    redis_client.ping()
    print("DEBUG: Redis connection test successful")
except Exception as e:
    print(f"DEBUG: Redis connection test failed: {e}")
    print(f"DEBUG: Attempted to connect to: {CELERY_BROKER_URL}")
    
    # Try alternative Redis connection methods
    alternative_urls = [
        os.environ.get('REDIS_URL'),
        os.environ.get('CELERY_BROKER_URL'),
        'redis://localhost:6379/0',
        'redis://redis:6379/0',
        'redis://django-cv-redis:6379/0'
    ]
    
    for alt_url in alternative_urls:
        if alt_url and alt_url != CELERY_BROKER_URL:
            try:
                print(f"DEBUG: Trying alternative Redis URL: {alt_url}")
                redis_client = redis.from_url(alt_url, socket_connect_timeout=5, socket_timeout=5)
                redis_client.ping()
                CELERY_BROKER_URL = alt_url
                CELERY_RESULT_BACKEND = alt_url
                print(f"DEBUG: Alternative Redis connection successful: {alt_url}")
                break
            except Exception as e2:
                print(f"DEBUG: Alternative Redis connection failed: {e2}")
    
    # If all alternatives fail, log the issue but don't fail startup
    if not redis_client or not hasattr(redis_client, 'ping'):
        print("DEBUG: All Redis connection attempts failed - Celery tasks may not work")

# Slide processing settings
SLIDES_WATCH_DIR = Path(os.environ.get('SLIDES_WATCH_DIR', BASE_DIR / 'incoming_slides'))
SLIDES_CONTENT_DIR = Path(os.environ.get('SLIDES_CONTENT_DIR', BASE_DIR / 'content'))

# Celery Beat schedule
CELERY_BEAT_SCHEDULE = {
    'scan-slides-folder-every-2-mins': {
        'task': 'tasksapp.tasks.scan_slides_folder',
        'schedule': 120.0,
    },
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
