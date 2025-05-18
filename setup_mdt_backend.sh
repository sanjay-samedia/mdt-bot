#!/bin/bash

# Exit on error
set -e

# Variables
APP_DIR="/home/ec2-user/mdt_backend"
PYTHON_VERSION="3.11"
VENV_DIR="$APP_DIR/venv"
CELERY_LOG="$APP_DIR/celery.log"
GUNICORN_LOG="$APP_DIR/gunicorn.log"

echo "==> Updating system packages..."
sudo yum update -y

echo "==> Installing system dependencies..."
sudo yum install -y gcc git postgresql-devel python3${PYTHON_VERSION} python3${PYTHON_VERSION}-devel

# Create symlinks for python3.11 and pip3.11 if needed
if ! command -v python3.11 &> /dev/null; then
  sudo amazon-linux-extras enable python3.8
  sudo yum install -y python3.8
fi

# Use fallback if python3.11 is not installed
PYTHON_BIN=$(command -v python3.11 || command -v python3.8)
PIP_BIN=$(command -v pip3.11 || command -v pip3.8)

echo "==> Creating project directory..."
mkdir -p $APP_DIR

echo "==> Cloning or copying project files to $APP_DIR..."
# git clone <your_repo_url> $APP_DIR
# or use: scp -r ./mdt_backend ec2-user@<ip>:/home/ec2-user/

echo "==> Creating virtual environment..."
$PYTHON_BIN -m venv $VENV_DIR

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
gunicorn traffic_bot_server.wsgi:application \
  --bind 0.0.0.0:8000 >> "$GUNICORN_LOG" 2>&1 &

echo "==> Starting Celery worker (connecting to Redis in Docker)..."
celery -A mdt_backend.traffic_bot_server worker \
  --concurrency=$(nproc) \
  -l info >> "$CELERY_LOG" 2>&1 &

echo "✅ Setup complete. Gunicorn and Celery are now running."


#-----TO MAKE THE SCRIPT EXECUTABLE-----#
#      >>> chmod +x setup_ec2.sh        #
#---------------------------------------#

#-----------TO RUN THE SCRIPT-----------#
#      >>> ./setup_ec2.sh               #
#---------------------------------------#