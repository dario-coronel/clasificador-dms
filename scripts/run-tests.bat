@echo off
echo ================================
echo   EDMS - Ejecutando Tests
echo ================================

cd backend

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Ejecutando tests...
pytest -v --tb=short

echo.
echo Tests completados.
pause