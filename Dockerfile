# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY mdt_backend/requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

# RUN python manage.py collectstatic --noinput

# Copy backend code
COPY mdt_backend .

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "traffic_bot_server.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
