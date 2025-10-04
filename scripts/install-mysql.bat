@echo off
echo ================================
echo   EDMS - Instalacion MySQL
echo ================================

echo.
echo Este script te ayudara a instalar MySQL en Windows
echo.

echo OPCION 1: MySQL Community Server (Recomendado)
echo 1. Ve a: https://dev.mysql.com/downloads/mysql/
echo 2. Descarga "MySQL Community Server" para Windows
echo 3. Ejecuta el instalador
echo 4. Durante la instalacion:
echo    - Elige "Developer Default" o "Server only"
echo    - Configura una contraseña para root
echo    - Anota la contraseña, la necesitaras
echo.

echo OPCION 2: XAMPP (Mas facil para desarrollo)
echo 1. Ve a: https://www.apachefriends.org/download.html
echo 2. Descarga XAMPP para Windows
echo 3. Instala XAMPP
echo 4. Inicia Apache y MySQL desde el panel de control
echo.

echo OPCION 3: Docker (Si tienes Docker instalado)
echo docker run --name mysql-edms -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=edms_db -p 3306:3306 -d mysql:8.0
echo.

echo ================================
echo   DESPUES DE INSTALAR MYSQL:
echo ================================
echo 1. Ejecuta: scripts\configure-database.bat
echo 2. O ejecuta manualmente: scripts\setup-database.sql
echo.
pause