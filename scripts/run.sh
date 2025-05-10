#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uvicorn recipick_app.asgi:application --host 0.0.0.0 --port 9000
