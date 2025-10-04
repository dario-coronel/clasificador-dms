@echo off
cd /d "%~dp0"
echo ====================================
echo Iniciando EDMS ML Backend...
echo ====================================
echo.

REM Verificar que Tesseract este instalado
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Tesseract OCR no encontrado.
    echo Ejecuta install_tesseract.bat para instalarlo.
    echo.
    pause
    exit /b 1
)

REM Crear directorio temporal si no existe
if not exist "temp_uploads" mkdir temp_uploads

REM Iniciar el servidor
echo [INFO] Iniciando servidor en http://localhost:8001...
echo [INFO] Documentacion disponible en http://localhost:8001/docs
echo.
echo OCR completo disponible con Tesseract.
echo Soporta imagenes, PDFs y archivos de texto.
echo.
echo Presiona Ctrl+C para detener el servidor.
echo.

python main.py
