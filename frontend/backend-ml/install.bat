@echo off
echo ====================================
echo EDMS ML Backend - Instalador
echo ====================================
echo.

echo [1/4] Verificando Tesseract OCR...
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Tesseract OCR no esta instalado.
    echo.
    echo Por favor, descarga e instala Tesseract OCR desde:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Recomendado: tesseract-ocr-w64-setup-5.3.3.20231005.exe
    echo Instalar en: C:\Program Files\Tesseract-OCR
    echo.
    echo Despues de instalar, agrega esta ruta al PATH del sistema.
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Tesseract OCR encontrado
    tesseract --version
    echo.
)

echo [2/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado.
    echo Por favor, instala Python 3.8 o superior.
    pause
    exit /b 1
) else (
    echo [OK] Python encontrado
    python --version
    echo.
)

echo [3/4] Creando directorios...
if not exist "temp_uploads" mkdir temp_uploads
echo [OK] Directorio temp_uploads creado
echo.

echo [4/4] Instalando dependencias Python...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas correctamente
echo.

echo ====================================
echo Instalacion completada exitosamente!
echo ====================================
echo.
echo Para iniciar el servidor ML, ejecuta:
echo   python main.py
echo.
echo La API estara disponible en:
echo   http://localhost:8001
echo   http://localhost:8001/docs (documentacion)
echo.
pause
