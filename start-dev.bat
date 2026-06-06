@echo off
:: =========================================================================
:: ZaryahPlus / Sakinah - Local Development Startup Script
:: =========================================================================
:: IMPORTANT: This script is for LOCAL DEVELOPMENT purposes ONLY.
:: It is NOT intended for production deployment. Production deployments
:: should use proper hosting platforms, process managers (e.g., Gunicorn, 
:: systemd), and proper reverse proxies (e.g., Nginx, Traefik).
:: =========================================================================

echo Starting ZaryahPlus Local Development Environment...

:: Start the Backend (FastAPI) in a new terminal window
echo Starting Backend (FastAPI on Uvicorn)...
start "ZaryahPlus Backend" cmd /k "cd backend && call .\venv\Scripts\activate && uvicorn app.main:app --reload"

:: Start the Frontend (Vite/React) in a new terminal window
echo Starting Frontend (Vite)...
start "ZaryahPlus Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both services have been launched in separate windows!
echo - Frontend usually runs on http://localhost:5173
echo - Backend usually runs on http://localhost:8000
echo.
echo Please check the opened terminal windows for logs and any startup errors.
echo Close the terminal windows to stop the servers.
pause
