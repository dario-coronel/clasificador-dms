@echo off
echo ====================================
echo Iniciando EDMS ML Backend...
echo ====================================
echo.

REM Verificar que Tesseract este instalado
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Tesseract OCR no encontrado.
    echo Ejecuta install.bat primero.
    pause
    exit /b 1
)

REM Crear directorio temporal si no existe
if not exist "temp_uploads" mkdir temp_uploads

REM Iniciar el servidor
echo [INFO] Iniciando servidor en http://localhost:8002...
echo [INFO] Documentacion disponible en http://localhost:8002/docs
echo.
echo Presiona Ctrl+C para detener el servidor.
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
