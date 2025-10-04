@echo off
echo ================================
echo   EDMS - MySQL con Docker
echo ================================

echo.
echo Iniciando MySQL en contenedor Docker...
echo.

docker run --name mysql-edms ^
  -e MYSQL_ROOT_PASSWORD=root123 ^
  -e MYSQL_DATABASE=edms_db ^
  -e MYSQL_USER=edms_user ^
  -e MYSQL_PASSWORD=edms_password123 ^
  -p 3306:3306 ^
  -d mysql:8.0

if %errorlevel% == 0 (
    echo.
    echo ================================
    echo   MySQL INICIADO EXITOSAMENTE
    echo ================================
    echo.
    echo Contenedor: mysql-edms
    echo Puerto: 3306
    echo Base de datos: edms_db
    echo Usuario: edms_user
    echo Contraseña: edms_password123
    echo.
    echo Esperando que MySQL inicie completamente...
    timeout /t 10 /nobreak > nul
    echo.
    echo MySQL esta listo para usar!
    echo Ahora puedes ejecutar: scripts\start-backend.bat
) else (
    echo.
    echo ERROR: No se pudo iniciar MySQL
    echo Verifica que Docker este ejecutandose
)

echo.
pause