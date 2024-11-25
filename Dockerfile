# Use Python 3.9 slim base image
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=Scheduler.settings

WORKDIR /app


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

COPY . .

# Collect static files and migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1


EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "Scheduler.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
