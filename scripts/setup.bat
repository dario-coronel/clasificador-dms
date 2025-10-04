@echo off
echo ================================
echo   EDMS - Configuracion Inicial
echo ================================

echo.
echo [1/4] Creando entorno virtual...
cd backend
python -m venv venv

echo.
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate

echo.
echo [3/4] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [4/4] Copiando configuracion...
if not exist .env (
    copy .env.example .env
    echo Archivo .env creado. Por favor, edita las configuraciones en backend/.env
)

echo.
echo ================================
echo   CONFIGURACION COMPLETADA
echo ================================
echo.
echo Proximos pasos:
echo 1. Edita backend/.env con tu configuracion de MySQL
echo 2. Ejecuta: scripts\start-backend.bat
echo 3. Abre http://localhost:8000/docs para ver la API
echo.
pause