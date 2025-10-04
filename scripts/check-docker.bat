@echo off
echo ========================================
echo   EDMS - Iniciar Docker Desktop
echo ========================================
echo.
echo Docker Desktop no esta ejecutandose.
echo.
echo PASOS PARA INICIAR DOCKER DESKTOP:
echo.
echo 1. Busca "Docker Desktop" en el menu de inicio de Windows
echo 2. Haz clic en "Docker Desktop" para iniciarlo
echo 3. Espera a que aparezca el icono de Docker en la bandeja del sistema
echo 4. El icono debe estar en verde (ejecutandose)
echo.
echo ALTERNATIVA - Iniciar desde linea de comandos:
echo.
echo Si tienes Docker Desktop instalado, ejecuta:
echo   "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo.
echo ========================================
echo   DESPUES DE INICIAR DOCKER DESKTOP:
echo ========================================
echo.
echo 1. Ejecuta: scripts\setup-mysql-docker.bat
echo 2. O sigue las instrucciones en pantalla
echo.
echo Presiona cualquier tecla cuando Docker Desktop este ejecutandose...
pause > nul

echo.
echo Verificando Docker...
docker ps
if %errorlevel% == 0 (
    echo.
    echo ✅ Docker Desktop esta ejecutandose!
    echo Ahora puedes ejecutar: scripts\setup-mysql-docker.bat
) else (
    echo.
    echo ❌ Docker Desktop aun no esta ejecutandose.
    echo Por favor, asegurate de que Docker Desktop este iniciado.
)

echo.
pause