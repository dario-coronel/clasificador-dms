# 🗄️ Configuración de Base de Datos MySQL para EDMS

## Opción 1: MySQL con Docker (Recomendado) 🐳

### Prerrequisitos
1. **Instalar Docker Desktop**:
   - Descarga desde: https://www.docker.com/products/docker-desktop
   - Instala y ejecuta Docker Desktop
   - Verifica que Docker esté ejecutándose (ícono en la bandeja del sistema)

### Comandos para configurar MySQL

```bash
# 1. Iniciar contenedor MySQL
docker run --name mysql-edms \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=edms_db \
  -e MYSQL_USER=edms_user \
  -e MYSQL_PASSWORD=edms_password123 \
  -p 3306:3306 \
  -d mysql:8.0

# 2. Verificar que el contenedor esté ejecutándose
docker ps

# 3. Para detener MySQL (cuando termines)
docker stop mysql-edms

# 4. Para reiniciar MySQL
docker start mysql-edms

# 5. Para conectarte a MySQL directamente
docker exec -it mysql-edms mysql -u edms_user -p
```

## Opción 2: MySQL Server Local 💾

### Instalación
1. **Descargar MySQL**:
   - Ve a: https://dev.mysql.com/downloads/mysql/
   - Descarga "MySQL Community Server" para Windows
   - Ejecuta el instalador

2. **Configuración durante instalación**:
   - Elige "Developer Default"
   - Configura contraseña para root
   - Recuerda la contraseña

### Configurar base de datos
```sql
-- Ejecuta en MySQL Workbench o línea de comandos
CREATE DATABASE edms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'edms_user'@'localhost' IDENTIFIED BY 'edms_password123';
GRANT ALL PRIVILEGES ON edms_db.* TO 'edms_user'@'localhost';
FLUSH PRIVILEGES;
```

## Opción 3: XAMPP (Más fácil para principiantes) 📦

### Instalación
1. **Descargar XAMPP**:
   - Ve a: https://www.apachefriends.org/download.html
   - Descarga XAMPP para Windows
   - Instala XAMPP

2. **Configurar**:
   - Abre el Panel de Control de XAMPP
   - Inicia Apache y MySQL
   - Haz clic en "Admin" junto a MySQL para abrir phpMyAdmin

3. **Crear base de datos**:
   - En phpMyAdmin, crea nueva base de datos: `edms_db`
   - Ve a "Usuarios" y crea: `edms_user` con contraseña `edms_password123`

## ⚙️ Configuración del Backend

Una vez que tengas MySQL ejecutándose, el archivo `.env` ya está configurado correctamente:

```env
DATABASE_URL=mysql+pymysql://edms_user:edms_password123@localhost:3306/edms_db
```

## 🚀 Probar la configuración

```bash
# Navegar al backend
cd c:\Clases\Clasificador-DMS\backend

# Activar entorno virtual
venv\Scripts\activate

# Iniciar el servidor
python main.py
```

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🔍 Verificar que funciona

1. **API Health Check**: http://localhost:8000/health
2. **Documentación Swagger**: http://localhost:8000/docs
3. **Documentación ReDoc**: http://localhost:8000/redoc

## 🆘 Problemas comunes

### Error de conexión a MySQL
- Verifica que MySQL esté ejecutándose
- Comprueba usuario y contraseña en `.env`
- Para Docker: `docker ps` debe mostrar `mysql-edms`

### Puerto 3306 ocupado
```bash
# Verificar qué está usando el puerto
netstat -ano | findstr :3306

# Para Docker, usar puerto diferente
docker run --name mysql-edms ... -p 3307:3306 ...
# Cambiar en .env: localhost:3307
```

### Error de Docker
- Asegúrate que Docker Desktop esté ejecutándose
- Reinicia Docker Desktop si es necesario

---

**¿Qué opción prefieres usar?** Te ayudo con la que elijas 🚀