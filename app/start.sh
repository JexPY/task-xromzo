#! /usr/bin/env sh
set -e

# Start Gunicorn
exec gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:3000 app:"create_app()" --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info