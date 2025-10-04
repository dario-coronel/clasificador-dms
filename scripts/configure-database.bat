@echo off
echo ================================
echo   EDMS - Configurar Base de Datos
echo ================================

echo.
echo Este script configurara la base de datos MySQL para EDMS
echo.

set /p mysql_password="Ingresa la contraseña de MySQL root: "

echo.
echo Ejecutando script de configuracion...
mysql -u root -p%mysql_password% < scripts\setup-database.sql

if %errorlevel% == 0 (
    echo.
    echo ================================
    echo   BASE DE DATOS CONFIGURADA
    echo ================================
    echo.
    echo La base de datos EDMS ha sido configurada exitosamente!
    echo.
    echo Detalles de conexion:
    echo - Base de datos: edms_db
    echo - Usuario: edms_user
    echo - Contraseña: edms_password123
    echo - Host: localhost
    echo - Puerto: 3306
    echo.
    echo Ahora puedes ejecutar: scripts\start-backend.bat
) else (
    echo.
    echo ERROR: No se pudo configurar la base de datos
    echo Verifica que MySQL este ejecutandose y que la contraseña sea correcta
)

echo.
pause