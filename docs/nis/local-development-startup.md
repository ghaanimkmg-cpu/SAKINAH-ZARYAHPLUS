# ZaryahPlus Local Development Startup Guide

This document explains how to quickly start the ZaryahPlus / Sakinah project locally for development and testing.

> **WARNING: NOT FOR PRODUCTION**  
> The provided `start-dev.bat` script is intended **strictly for local development**. It does not implement production security, process management, or scaling. Do not use this script to deploy the application to a live server.

## Prerequisites

Before using the startup script, ensure your local environment is prepared:

1. **Node.js** (v18+ recommended) is installed.
2. **Python** (v3.10+ recommended) is installed.
3. The backend virtual environment is created at `backend/venv`.
4. All dependencies are installed.

### Installing Dependencies (First Time Setup)

**Frontend:**
```bash
cd frontend
npm install
```

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
*(If the backend `venv` folder does not exist, you must create it using the command above before starting the server.)*

## Using `start-dev.bat`

To launch both the frontend and backend servers simultaneously:

1. Open the project root folder in Windows Explorer or your IDE.
2. Double-click the `start-dev.bat` file, or run `.\start-dev.bat` in your terminal.
3. Two new terminal windows will open automatically:
   - One window will activate the Python virtual environment and start the FastAPI backend via Uvicorn.
   - The other window will start the Vite frontend via `npm run dev`.
4. The script will wait a few seconds and then **automatically open your default browser** to the Sakinah frontend at: `http://localhost:5173/sakinah`.
   - *Note: If the page does not load immediately because the server is still starting up, simply wait a few seconds and refresh.*

## Default Ports

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Backend OpenAPI Docs:** http://localhost:8000/docs
- **Backend Health Check:** http://localhost:8000/health

## Architecture: Frontend-Backend Connection

The Sakinah frontend connects to the NIS backend using relative API paths (e.g., `/api/v1/nis/eligibility/me`). During local development, the Vite server uses a **proxy configuration** (`vite.config.ts`) to forward these requests to the local backend running on `http://127.0.0.1:8000`.

### Development Preview Mode

If the frontend attempts to make an API call and the backend is unreachable (e.g., the backend server is not running or the proxy fails), the UI will gracefully fall back to **Development Preview Mode**. 

- **Why it appears:** It prevents the frontend from crashing during local UI development when the backend isn't needed. Safe mock data is used instead.
- **How to fix it:** If you see "Backend is not connected, so safe demo data is being used" while expecting real data:
  1. Ensure the backend is running via `start-dev.bat`.
  2. Verify the backend health check at http://127.0.0.1:8000/health is returning a success response.
  3. Ensure the frontend is being accessed via `http://localhost:5173` so the proxy can correctly route `/api` and `/health` requests to `127.0.0.1:8000`.

To stop the development servers, simply close the two newly opened terminal windows.

## Troubleshooting Build Issues

If building for production (`npm run build`) or running Vite encounters an out-of-memory error (e.g. `fatal error: out of memory`), you must increase the Node.js memory limit:

**Windows PowerShell:**
```powershell
$env:NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

**Linux/macOS:**
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```
