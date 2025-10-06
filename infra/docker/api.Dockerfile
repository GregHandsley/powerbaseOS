FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime & tooling needed by Sprint 3
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic-settings \
    email-validator \
    sqlalchemy \
    asyncpg \
    alembic \
    passlib[bcrypt] \
    "bcrypt==3.2.2" \
    python-jose[cryptography]

# Copy app code
COPY apps/api /app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]