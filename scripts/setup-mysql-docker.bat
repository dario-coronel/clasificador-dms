@echo off
echo ========================================
echo   EDMS - Configurar MySQL con Docker
echo ========================================
echo.

echo Verificando Docker Desktop...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop no esta ejecutandose.
    echo.
    echo Por favor:
    echo 1. Inicia Docker Desktop desde el menu de Windows
    echo 2. Espera a que el icono aparezca en verde en la bandeja del sistema
    echo 3. Ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)

echo ✅ Docker Desktop esta ejecutandose.
echo.

echo Verificando si ya existe el contenedor mysql-edms...
docker ps -a | findstr mysql-edms >nul 2>&1
if %errorlevel% == 0 (
    echo.
    echo El contenedor mysql-edms ya existe.
    echo ¿Quieres eliminarlo y crear uno nuevo? (s/n)
    set /p respuesta="Respuesta: "
    if /i "%respuesta%"=="s" (
        echo Eliminando contenedor existente...
        docker rm -f mysql-edms
        echo Contenedor eliminado.
        echo.
    ) else (
        echo Iniciando contenedor existente...
        docker start mysql-edms
        goto :success
    )
)

echo Creando nuevo contenedor MySQL...
echo.
echo Configuracion:
echo - Nombre: mysql-edms
echo - Puerto: 3306
echo - Base de datos: edms_db  
echo - Usuario: edms_user
echo - Contraseña: edms_password123
echo - Contraseña root: root123
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
    echo ✅ Contenedor MySQL creado exitosamente!
    echo.
    echo Esperando que MySQL inicie completamente...
    echo (Esto puede tomar 30-60 segundos la primera vez)
    
    :wait_loop
    timeout /t 5 /nobreak >nul
    docker exec mysql-edms mysqladmin ping -h localhost -u root -proot123 >nul 2>&1
    if %errorlevel% neq 0 (
        echo Esperando MySQL...
        goto :wait_loop
    )
    
    :success
    echo.
    echo ========================================
    echo   ✅ MYSQL CONFIGURADO EXITOSAMENTE
    echo ========================================
    echo.
    echo 📊 Informacion de conexion:
    echo   Host: localhost
    echo   Puerto: 3306
    echo   Base de datos: edms_db
    echo   Usuario: edms_user
    echo   Contraseña: edms_password123
    echo.
    echo 🔧 Comandos utiles:
    echo   Ver logs: docker logs mysql-edms
    echo   Detener: docker stop mysql-edms
    echo   Iniciar: docker start mysql-edms
    echo   Eliminar: docker rm -f mysql-edms
    echo.
    echo 🚀 PROXIMO PASO:
    echo   Ejecuta: scripts\start-backend-full.bat
    echo   Para iniciar la API completa con base de datos
    echo.
) else (
    echo.
    echo ❌ Error al crear el contenedor MySQL.
    echo Verifica que Docker Desktop este ejecutandose correctamente.
)

echo.
pause