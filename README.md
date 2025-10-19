# Async Demo with Django, Celery, Redis, and Flower

## Prerequisites
- Redis server running locally (default: `redis://localhost:6379/0`)

## Setup
```bash
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
```

## Run
- Django dev server:
```bash
.venv\Scripts\python manage.py runserver 0.0.0.0:8000
```
- Celery worker:
```bash
.venv\Scripts\celery -A async_demo worker -l info
```
- Flower (monitor in browser at `http://localhost:5555`):
```bash
.venv\Scripts\celery -A async_demo flower --port=5555
```

Open `http://localhost:8000` to try tasks:
- Add two numbers
- Count words

If Redis is not local, set env vars:
```bash
set CELERY_BROKER_URL=redis://<host>:<port>/<db>
set CELERY_RESULT_BACKEND=%CELERY_BROKER_URL%
```


