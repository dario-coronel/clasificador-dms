@echo off
echo ====================================
echo Instalador de Tesseract OCR
echo ====================================
echo.
echo Tesseract OCR es necesario para el procesamiento de imagenes.
echo.
echo Pasos para instalar Tesseract OCR:
echo.
echo 1. Descarga el instalador desde:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 2. Ejecuta el instalador como administrador
echo.
echo 3. Instala en la ruta por defecto:
echo    C:\Program Files\Tesseract-OCR\
echo.
echo 4. Agrega al PATH del sistema:
echo    C:\Program Files\Tesseract-OCR\
echo.
echo 5. Reinicia la terminal y ejecuta este script nuevamente
echo    para verificar la instalacion.
echo.
echo ====================================
echo.

REM Verificar si Tesseract esta instalado
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Tesseract NO esta instalado.
    echo.
    echo Por favor, instala Tesseract OCR siguiendo los pasos arriba.
    echo.
    pause
    start https://github.com/UB-Mannheim/tesseract/wiki
    exit /b 1
) else (
    echo ✅ Tesseract esta instalado correctamente!
    echo.
    tesseract --version
    echo.
    echo Ahora puedes usar OCR con imagenes y PDFs escaneados.
    echo.
    pause
)