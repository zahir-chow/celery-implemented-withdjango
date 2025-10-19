## Celery/Flower: “No data showing” – Incident Report and Fix

### Context
- Stack: Django + Celery 5.5, Redis broker/result backend, Flower 2.0 (Docker Compose)
- Services: `web`, `celery` worker (`-E` enabled), `beat`, `redis`, `flower`

### Symptom
- Flower UI at http://localhost:5555 loaded, but showed no tasks/metrics.
- “Workers” list was empty or counters stayed at 0 despite running tasks from the app.

### What we saw in logs
- Worker was healthy and emitting events:
  - `task events: ON`
  - Connected to `redis://redis:6379/0`
  - Tasks received and succeeded.
- Flower initially failed to connect and kept retrying with `ConnectionRefusedError` from kombu:
  - `kombu.exceptions.OperationalError: [Errno 111] Connection refused`
- After first change, another error appeared:
  - `sh: flower: not found` (binary not in PATH for the chosen exec form)
- After a second change, Flower started but warned about incorrect CLI arg order:
  - `You have incorrectly specified the following celery arguments after flower command: ['--result-backend']`

### Root cause
- Flower container was not reliably picking up the broker/backend from env alone and/or defaulted to AMQP when CLI args were not provided correctly.
- Wrong executable/command form (`flower` not found) and misordered Celery CLI arguments caused Flower not to start or not to connect correctly to Redis.

### Fix applied
1) Keep the worker emitting events (already correct):
   - Worker command includes `-E` in `docker-compose.yml`.
2) Start Flower with explicit Celery CLI and correct argument ordering, pointing to Redis broker:
   - Final command used:
     ```bash
     celery --broker=redis://redis:6379/0 flower --port=5555
     ```
   - Result backend is provided via environment: `FLOWER_RESULT_BACKEND=redis://redis:6379/0`.
3) Restart Flower:
   - `docker compose up -d flower`

### Verification steps
1) Check Flower logs:
   ```bash
   docker compose logs flower --no-color --tail=200
   ```
   Expect:
   - `Visit me at http://0.0.0.0:5555`
   - `Broker: redis://redis:6379/0`
   - `Connected to redis://redis:6379/0`
2) Confirm worker appears in Flower UI under Workers.
3) Trigger tasks from the app (e.g., `add`, `count_words`).
4) Observe Dashboard counters (Succeeded/Failed) and Task list update.

### Quick failure test (to see Failed count)
- Trigger a task with invalid input (e.g., send a string where an int is expected) to force a failure and see the Failed counter increment.

### Notes and alternatives
- If you prefer to pass backend via CLI too, use correct ordering:
  ```bash
  celery --broker=redis://redis:6379/0 --result-backend=redis://redis:6379/0 flower --port=5555
  ```
- Ensure all services use the same Redis DB/index (here: `redis://redis:6379/0`).
- If Flower shows no workers, ensure the worker is up, connected to the same broker, and that `-E` is enabled.


