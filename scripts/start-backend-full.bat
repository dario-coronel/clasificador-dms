@echo off
echo ========================================
echo   EDMS - API Completa con MySQL
echo ========================================
echo.

echo Verificando MySQL...
docker ps | findstr mysql-edms >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ El contenedor MySQL no esta ejecutandose.
    echo.
    echo Por favor ejecuta primero: scripts\setup-mysql-docker.bat
    echo.
    pause
    exit /b 1
)

echo ✅ MySQL esta ejecutandose.
echo.

echo Verificando conexion a la base de datos...
docker exec mysql-edms mysqladmin ping -h localhost -u edms_user -pedms_password123 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No se puede conectar a MySQL.
    echo MySQL puede estar iniciando aun. Esperando...
    timeout /t 10 /nobreak >nul
)

cd backend

echo Verificando dependencias de Python...
python -c "import fastapi, sqlalchemy, pymysql" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias de Python...
    pip install fastapi uvicorn sqlalchemy pymysql cryptography python-jose passlib python-multipart aiofiles pillow
)

echo.
echo ========================================
echo   🚀 INICIANDO EDMS API COMPLETA
echo ========================================
echo.
echo 📊 MySQL: mysql-edms (localhost:3306)
echo 🌐 API: http://localhost:8000
echo 📖 Docs: http://localhost:8000/docs  
echo 📚 ReDoc: http://localhost:8000/redoc
echo.
echo Para detener: Ctrl+C
echo.

python main.py