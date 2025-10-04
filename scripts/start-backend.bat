@echo off
echo ================================
echo   EDMS - Iniciando Backend
echo ================================

cd backend

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Iniciando servidor FastAPI...
echo API disponible en: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.

python main.py