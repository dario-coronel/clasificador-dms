-- Script de configuración de base de datos MySQL para EDMS
-- Ejecuta este script en MySQL Workbench o línea de comandos

-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS edms_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'edms_user'@'localhost' IDENTIFIED BY 'edms_password123';

-- 3. Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON edms_db.* TO 'edms_user'@'localhost';

-- 4. Aplicar cambios
FLUSH PRIVILEGES;

-- 5. Verificar la configuración
USE edms_db;
SELECT 'Base de datos EDMS configurada correctamente!' AS status;

-- 6. Mostrar información de la base de datos
SHOW DATABASES LIKE 'edms_db';
SELECT USER, HOST FROM mysql.user WHERE USER = 'edms_user';