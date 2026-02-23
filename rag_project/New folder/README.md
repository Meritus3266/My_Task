# Policy Assistant API - FastAPI Backend

A production-ready FastAPI backend for an Agentic RAG system for policy document Q&A.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit the `.env` file to set your configuration:

```env
ENV=development          # development or production
DEBUG=False             # Enable/disable debug mode
HOST=0.0.0.0           # Server host
PORT=8000              # Server port
LOG_LEVEL=info         # Logging level
WORKERS=1              # Number of worker processes (use 4+ for production)
OPENAI_API_KEY=xxx     # Your OpenAI API key
```

## Running the Application

### Development Mode (with auto-reload)
```bash
# Using Python directly
python fastapi_backend.py

# Or using uvicorn
uvicorn fastapi_backend:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode (no reload, multiple workers)
**Windows:**
```batch
start_production.bat
```

**Linux/Mac:**
```bash
bash start_production.sh
```

**Or manually:**
```bash
ENV=production WORKERS=4 uvicorn fastapi_backend:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level warning
```

## API Documentation

Once running, access the API documentation at:
- **Development**: http://localhost:8000/docs (Swagger UI)
- **Development**: http://localhost:8000/redoc (ReDoc)

## Key Endpoints

- `POST /chat` - Send a chat message
- `POST /sessions` - Create a new session
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}/history` - Get conversation history
- `WS /ws/{session_id}` - WebSocket for real-time chat
- `GET /health` - Health check
- `GET /system/stats` - System statistics

## Production Considerations

### ✓ What's Configured
- ✓ Proper import string for uvicorn (`uvicorn fastapi_backend:app`)
- ✓ Environment-based configuration (development/production)
- ✓ Multiple worker processes for production
- ✓ Logging configuration
- ✓ Error handling with proper HTTP exceptions
- ✓ CORS middleware for frontend communication
- ✓ Conditional docs endpoint (only in development)
- ✓ Session management

### Additional Recommendations for Production

1. **Database**: Replace in-memory session storage with persistent database (PostgreSQL, MongoDB, etc.)

2. **Authentication**: Add JWT or OAuth2 authentication
   ```python
   from fastapi.security import HTTPBearer
   ```

3. **Rate Limiting**: Add rate limiting middleware
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   ```

4. **Monitoring**: Add health checks and monitoring
   ```python
   from prometheus_client import Counter, Histogram
   ```

5. **HTTPS**: Deploy with HTTPS/SSL (using nginx or similar)

6. **Container**: Use Docker for deployment
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "fastapi_backend:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
   ```

7. **Reverse Proxy**: Use nginx or similar for load balancing

8. **Environment Secrets**: Use proper secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)

## Troubleshooting

### Warning: "You must pass the application as an import string..."
This is now fixed! The app uses the proper import string format:
```python
uvicorn.run("fastapi_backend:app", ...)
```

### Port already in use
Change the PORT in .env or use:
```bash
uvicorn fastapi_backend:app --port 8001
```

### Module not found errors
Ensure you're in the correct directory and all dependencies are installed:
```bash
pip install -r requirements.txt
```
