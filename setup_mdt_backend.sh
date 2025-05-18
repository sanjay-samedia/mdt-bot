#!/bin/bash

# Exit on error
set -e

# Variables
APP_DIR="/home/ubuntu/mdt_backend"
PYTHON_VERSION="3.11"
VENV_DIR="$APP_DIR/venv"
CELERY_LOG="$APP_DIR/celery.log"
GUNICORN_LOG="$APP_DIR/gunicorn.log"

echo "==> Updating system packages..."
sudo apt-get update

echo "==> Installing system dependencies..."
sudo apt-get install -y python${PYTHON_VERSION} python3-pip python3-venv gcc libpq-dev

echo "==> Creating project directory..."
mkdir -p $APP_DIR

echo "==> Cloning or copying project files to $APP_DIR..."
# You can use git clone or scp here.
# git clone <your_repo_url> $APP_DIR
# Or manually copy using: scp -r ./mdt_backend ubuntu@<your-ec2-ip>:/home/ubuntu/

echo "==> Creating virtual environment..."
python${PYTHON_VERSION} -m venv $VENV_DIR

echo "==> Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "==> Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

echo "==> Applying database migrations..."
cd $APP_DIR
python manage.py migrate

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn server..."
# Run Gunicorn in background and write logs to gunicorn.log
gunicorn traffic_bot_server.wsgi:application \
  --bind 0.0.0.0:8000 >> "$GUNICORN_LOG" 2>&1 &

echo "==> Starting Celery worker (connecting to Redis in Docker)..."
# Run Celery in background and write logs to celery.log
celery -A mdt_backend.traffic_bot_server worker \
  --concurrency=32 \
  -l info >> "$CELERY_LOG" 2>&1 &

echo "✅ Setup complete. Gunicorn and Celery are now running."


#-----TO MAKE THE SCRIPT EXECUTABLE-----#
#      >>> chmod +x setup_ec2.sh        #
#---------------------------------------#

#-----------TO RUN THE SCRIPT-----------#
#      >>> ./setup_ec2.sh               #
#---------------------------------------#