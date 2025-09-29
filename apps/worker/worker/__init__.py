from celery import Celery
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

# rename celery_app -> celery so Celery CLI can find it
celery = Celery("powerbase_worker", broker=redis_url, backend=redis_url)

@celery.task
def health_check():
    return "ok"