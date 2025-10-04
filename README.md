# Document Management System (EDMS)

Sistema de gestión documental completo construido con **FastAPI** (backend), **React** (frontend) y **MySQL** (base de datos).

## 🚀 Características

- **Gestión de documentos**: Subida, almacenamiento y organización de archivos
- **Autenticación segura**: JWT tokens con roles y permisos
- **OCR integrado**: Extracción automática de texto de documentos
- **Búsqueda avanzada**: Filtros por contenido, metadatos y fechas
- **Versionado**: Control de versiones de documentos
- **API REST**: Documentación automática con Swagger/OpenAPI
- **Interfaz moderna**: Dashboard responsivo con React

## 📁 Estructura del Proyecto

```
📁 Clasificador-DMS/
├── 📁 backend/              # FastAPI application
│   ├── 📁 app/
│   │   ├── 📁 api/          # API endpoints
│   │   ├── 📁 core/         # Core functionality (config, db, security)
│   │   ├── 📁 models/       # SQLAlchemy models
│   │   ├── 📁 schemas/      # Pydantic schemas
│   │   └── 📁 services/     # Business logic
│   ├── 📁 tests/            # Test suite
│   ├── main.py              # FastAPI app entry point
│   └── requirements.txt     # Python dependencies
├── 📁 frontend/             # React application (próximamente)
├── 📁 docker/               # Docker configuration
├── 📁 docs/                 # Documentation
└── 📁 scripts/              # Deployment scripts
```

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **JWT**: Autenticación con tokens
- **Tesseract OCR**: Extracción de texto

### Frontend (próximamente)
- **React**: Interfaz de usuario
- **Vite**: Build tool rápido
- **Tailwind CSS**: Estilos utilitarios
- **React Query**: Gestión de estado del servidor

### Base de Datos
- **MySQL**: Base de datos relacional principal
- **Redis**: Cache y tareas en background

## 📋 Prerequisitos

- Python 3.8+
- MySQL 8.0+
- Node.js 16+ (para frontend)
- Git

## ⚡ Instalación Rápida

### 1. Configurar Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus configuraciones
```

### 2. Configurar Base de Datos MySQL

```sql
-- Crear base de datos
CREATE DATABASE edms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario
CREATE USER 'edms_user'@'localhost' IDENTIFIED BY 'edms_password';
GRANT ALL PRIVILEGES ON edms_db.* TO 'edms_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Ejecutar Backend

```bash
# Desde el directorio backend
python main.py
```

El backend estará disponible en: http://localhost:8000

### 4. Acceder a la Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Database
DATABASE_URL=mysql+pymysql://edms_user:edms_password@localhost:3306/edms_db

# Security
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB

# OCR
TESSERACT_PATH=tesseract
OCR_LANGUAGES=eng,spa
```

## 📚 API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario

### Usuarios
- `GET /api/v1/users/me` - Perfil actual
- `PUT /api/v1/users/me` - Actualizar perfil
- `PUT /api/v1/users/me/password` - Cambiar contraseña

### Documentos
- `POST /api/v1/documents/upload` - Subir documento
- `GET /api/v1/documents/` - Listar documentos
- `GET /api/v1/documents/{id}` - Obtener documento
- `PUT /api/v1/documents/{id}` - Actualizar documento
- `DELETE /api/v1/documents/{id}` - Eliminar documento

## 🧪 Testing

```bash
# Ejecutar tests
cd backend
pytest

# Tests con coverage
pytest --cov=app tests/
```

## 🚀 Próximos Pasos

1. ✅ Backend FastAPI con autenticación
2. ⏳ Frontend React con dashboard
3. ⏳ Integración OCR con Tesseract
4. ⏳ Búsqueda full-text
5. ⏳ Sistema de versiones
6. ⏳ Notificaciones en tiempo real
7. ⏳ Dockerización completa

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

¿Problemas o preguntas? Abre un [issue](https://github.com/tu-usuario/edms/issues) o contacta al equipo de desarrollo.

---

**¡Construyamos el mejor sistema de gestión documental juntos! 📄✨**