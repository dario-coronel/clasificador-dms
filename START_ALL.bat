@echo off
echo ========================================
echo    EDMS - Sistema Completo
echo ========================================
echo.
echo Iniciando servicios...
echo.

REM Verificar Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado
    echo Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo Instala Python desde: https://www.python.org/
    pause
    exit /b 1
)

echo [1/2] Iniciando Backend ML en puerto 8001...
start "Backend ML" cmd /k "cd /d %~dp0frontend\backend-ml && python run_server.py"
timeout /t 3 /nobreak >nul

echo [2/2] Iniciando Frontend en puerto 3000...
start "Frontend React" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    Servicios Iniciados!
echo ========================================
echo.
echo Frontend:          http://localhost:3000
echo Backend ML:        http://localhost:8001
echo Docs API ML:       http://localhost:8001/docs
echo.
echo Para detener los servicios:
echo - Presiona Ctrl+C en cada ventana
echo.
echo Abriendo el navegador en 5 segundos...
timeout /t 5 /nobreak >nul
start http://localhost:3000
echo.
pause
