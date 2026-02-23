#!/bin/bash
# Production startup script for FastAPI backend

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Set production environment if not already set
export ENV=${ENV:-production}
export WORKERS=${WORKERS:-4}

echo "Starting Policy Assistant API in ${ENV} mode..."
echo "Workers: ${WORKERS}"
echo "Port: ${PORT}"

# Run with uvicorn
uvicorn fastapi_backend:app \
    --host ${HOST} \
    --port ${PORT} \
    --workers ${WORKERS} \
    --log-level ${LOG_LEVEL} \
    --access-log
