# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Set work directory
WORKDIR /app

# Install system dependencies for Chromium and Python
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    chromium \
    libx11-xcb1 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY mdt_backend/requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

# Copy backend code
COPY mdt_backend .

# Expose port
EXPOSE 8000

# Run server (for backend service)
CMD ["gunicorn", "traffic_bot_server.wsgi:application", "--bind", "0.0.0.0:8000"]