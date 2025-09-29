FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# Use uv (already added via lock in repo later; here we just pip install)
RUN pip install --no-cache-dir uvicorn fastapi

# Copy app code
COPY apps/api /app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]