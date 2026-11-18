@echo off
setlocal
cd /d "%~dp0"

if not exist ".env" (
    echo Missing .env file.
    echo Copy .env.example to .env, add your credentials, and run start.bat again.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create the virtual environment. Check that Python 3.10 or newer is installed.
        pause
        exit /b 1
    )
)

"venv\Scripts\python.exe" -c "import fastapi, uvicorn, pydantic, httpx, dotenv" >nul 2>&1
if errorlevel 1 (
    echo Installing project dependencies...
    "venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
)

echo Starting the API at http://localhost:4000
"venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 4000