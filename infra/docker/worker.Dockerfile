FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN pip install --no-cache-dir celery[redis] redis

COPY apps/worker /app

CMD ["celery", "-A", "worker", "worker", "-l", "info"]