@echo off
REM Production startup script for FastAPI backend (Windows)

REM Load environment variables from .env if it exists
if exist .env (
    for /f "tokens=*" %%i in (.env) do set %%i
)

REM Set production defaults
if not defined ENV set ENV=production
if not defined WORKERS set WORKERS=4
if not defined HOST set HOST=0.0.0.0
if not defined PORT set PORT=8000
if not defined LOG_LEVEL set LOG_LEVEL=warning

echo Starting Policy Assistant API in %ENV% mode...
echo Workers: %WORKERS%
echo Port: %PORT%

REM Run with uvicorn
uvicorn fastapi_backend:app ^
    --host %HOST% ^
    --port %PORT% ^
    --workers %WORKERS% ^
    --log-level %LOG_LEVEL% ^
    --access-log

pause
