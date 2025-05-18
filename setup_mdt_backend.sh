#!/bin/bash

set -e

APP_DIR="/home/ec2-user/mdt_backend"
VENV_DIR="$APP_DIR/venv"
CELERY_LOG="$APP_DIR/celery.log"
GUNICORN_LOG="$APP_DIR/gunicorn.log"

echo "==> Updating system packages..."
sudo dnf update -y

echo "==> Installing system dependencies..."
sudo dnf install -y gcc git postgresql-devel python3 python3-devel

echo "==> Creating project directory..."
mkdir -p $APP_DIR

echo "==> Copy or clone your project into $APP_DIR before running further steps."
# scp -r ./mdt_backend ec2-user@<IP>:/home/ec2-user/

echo "==> Creating virtual environment..."
python3 -m venv $VENV_DIR

echo "==> Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "==> Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

echo "==> Running migrations..."
cd $APP_DIR
python manage.py migrate

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
gunicorn traffic_bot_server.wsgi:application \
  --bind 0.0.0.0:8000 >> "$GUNICORN_LOG" 2>&1 &

echo "==> Starting Celery..."
celery -A mdt_backend.traffic_bot_server worker \
  --concurrency=$(nproc) -l info >> "$CELERY_LOG" 2>&1 &

echo "✅ Backend is now running with Gunicorn and Celery."



#-----TO MAKE THE SCRIPT EXECUTABLE-----#
#      >>> chmod +x setup_ec2.sh        #
#---------------------------------------#

#-----------TO RUN THE SCRIPT-----------#
#      >>> ./setup_ec2.sh               #
#---------------------------------------#