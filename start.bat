@echo off
title DRS Alarms - System Startup
color 0A

echo.
echo ============================================================
echo    DRS ALARMS 5G - AUTHENTICATION + DASHBOARD
echo ============================================================
echo.
echo Starting servers...
echo.

echo [1/2] Starting Flask Login Server (Port 5000)...
start "Flask Login Server" cmd /k "cd /d %~dp0 && python app.py"
timeout /t 4 /nobreak > nul

echo [2/2] Starting Streamlit Dashboard (Port 8501)...
start "Streamlit Dashboard" cmd /k "cd /d %~dp0 && streamlit run main.py"
timeout /t 3 /nobreak > nul

echo.
echo ============================================================
echo    SERVERS ARE STARTING...
echo ============================================================
echo.
echo Flask Login:      http://localhost:5000
echo Streamlit Dashboard: http://localhost:8501
echo.
echo CREDENTIALS:
echo    Admin:    admin / admin123
echo    Hazem:    hazemblg / hazem1234
echo    Operator: operator / operator123
echo.
echo ============================================================
echo.
echo Opening login page in browser...
timeout /t 3 /nobreak > nul

start http://localhost:5000

echo.
echo ============================================================
echo    SYSTEM IS READY!
echo ============================================================
echo.
echo 1. Login at: http://localhost:5000
echo 2. After login, you will be redirected to the dashboard
echo.
echo Keep the server windows open!
echo Close this window when you're done.
echo.
pause

