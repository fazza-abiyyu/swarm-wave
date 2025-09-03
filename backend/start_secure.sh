#!/bin/bash

# Security-enhanced startup script for production

export FLASK_ENV=production
export FLASK_DEBUG=False

# Remove server identification headers
export SERVER_SOFTWARE=""

# Set security environment variables
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Run with Gunicorn for production security
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${WORKERS:-4} \
    --timeout ${TIMEOUT:-300} \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance \
    app:app
