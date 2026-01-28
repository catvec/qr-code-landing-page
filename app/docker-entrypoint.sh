#!/bin/sh
set -euo pipefail

WORKERS=${WORKERS:-3}
PORT=${PORT:-8000}

echo "Starting Gunicorn with $WORKERS workers on port $PORT"

exec gunicorn --bind 0.0.0.0:${PORT} --workers "$WORKERS" qrlanding.wsgi:application
