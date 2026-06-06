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

## Default Ports

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Backend OpenAPI Docs:** http://localhost:8000/docs

To stop the development servers, simply close the two newly opened terminal windows.
