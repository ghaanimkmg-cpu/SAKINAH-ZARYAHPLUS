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
echo Both services are launching in separate windows!
echo Please keep the terminal windows open. Close them to stop the servers.
echo.
echo Waiting a few seconds for servers to start before opening the browser...
timeout /t 6 /nobreak >nul

:: Automatically open Sakinah frontend
echo Opening Sakinah frontend in your default browser...
echo If the browser opens before the server is ready, just refresh the page after a few seconds.
start http://localhost:5173/sakinah
echo.
pause
