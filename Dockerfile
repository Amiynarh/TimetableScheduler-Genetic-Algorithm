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
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Collect static files 
RUN python manage.py collectstatic --noinput --clear || true


EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "3", "Scheduler.wsgi:application"]
