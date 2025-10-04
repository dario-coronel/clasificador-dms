@echo off
echo ====================================
echo EDMS ML Backend - Instalacion Basica
echo (Sin soporte OCR de imagenes)
echo ====================================
echo.

echo [1/3] Verificando Python...
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

echo [2/3] Creando directorios...
if not exist "temp_uploads" mkdir temp_uploads
echo [OK] Directorio temp_uploads creado
echo.

echo [3/3] Instalando dependencias Python (version basica)...
python -m pip install --upgrade pip
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 PyPDF2==3.0.1 scikit-learn==1.3.2 joblib==1.3.2 numpy==1.26.2 pandas==2.1.3 python-multipart
if %errorlevel% neq 0 (
    echo [ERROR] Fallo la instalacion de dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas correctamente
echo.

echo ====================================
echo Instalacion completada!
echo ====================================
echo.
echo NOTA: Esta version NO incluye OCR de imagenes.
echo Solo procesa archivos de texto y PDFs con texto.
echo.
echo Para procesar imagenes escaneadas, instala Tesseract OCR:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Para iniciar el servidor ML, ejecuta:
echo   python main_lite.py
echo.
echo La API estara disponible en:
echo   http://localhost:8001
echo   http://localhost:8001/docs (documentacion)
echo.
pause
