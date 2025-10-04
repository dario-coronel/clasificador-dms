# 📄 Clasificador DMS - Sistema de Gestión Documental Inteligente

Sistema completo de gestión documental con **clasificación automática mediante Machine Learning**, construido con **FastAPI** (backend), **React + TypeScript** (frontend) y **MySQL** (base de datos).

## 🚀 Características Principales

### 🤖 Clasificación Inteligente con ML
- **12 categorías de documentos**: Contrato, Contrato de Granos, Informe, Factura, Remito, Nota de Crédito, Nota de Débito, Política, Manual, Orden de Compra, Recibo, Otro
- **Clasificación automática**: Utiliza algoritmos de Machine Learning (TF-IDF + Multinomial Naive Bayes) para clasificar documentos al momento de subirlos
- **Entrenamiento automático**: El modelo se mejora automáticamente con cada documento aprobado por los usuarios
- **Servicio ML independiente**: Servicio FastAPI dedicado (puerto 8002) para procesamiento de ML

### 📤 Importación y Gestión de Documentos
- **Importación masiva**: Sube múltiples documentos PDF simultáneamente
- **Vista previa y revisión**: Revisa la clasificación sugerida antes de aprobar
- **Corrección manual**: Modifica la categoría si la clasificación automática no es correcta
- **Almacenamiento organizado**: Los documentos se guardan en `backend/uploads/` con estructura organizada

### 🔍 Búsqueda Avanzada
- **Filtros múltiples**: Busca por fecha, proveedor, CUIT y tipo de documento
- **Búsqueda por texto**: Encuentra documentos por su contenido
- **Resultados instantáneos**: Interfaz reactiva con resultados en tiempo real

### 🔐 Autenticación y Seguridad
- **JWT tokens**: Autenticación segura con tokens de acceso
- **Registro e inicio de sesión**: Sistema completo de usuarios
- **Protección de rutas**: Endpoints protegidos por autenticación

### 💻 Interfaz Moderna
- **Dashboard responsivo**: Interfaz limpia y moderna con React + Tailwind CSS
- **Experiencia de usuario fluida**: Navegación intuitiva entre secciones
- **Feedback visual**: Toasts y notificaciones para confirmar acciones
- **Diseño adaptable**: Funciona perfectamente en desktop y dispositivos móviles

## 📁 Estructura del Proyecto

```
📁 Clasificador-DMS/
├── 📁 backend/                    # Backend FastAPI (Puerto 8000)
│   ├── 📁 app/
│   │   ├── 📁 api/                # API endpoints REST
│   │   │   └── 📁 api_v1/
│   │   │       └── 📁 endpoints/  # Auth, Documents, Users
│   │   ├── 📁 core/               # Configuración y seguridad
│   │   │   ├── config.py          # Variables de entorno
│   │   │   ├── database.py        # Conexión a MySQL
│   │   │   └── security.py        # JWT y encriptación
│   │   ├── 📁 models/             # Modelos SQLAlchemy
│   │   │   ├── user.py            # Modelo de usuarios
│   │   │   └── document.py        # Modelo de documentos
│   │   ├── 📁 schemas/            # Schemas Pydantic
│   │   └── 📁 services/           # Lógica de negocio
│   ├── 📁 uploads/                # Almacenamiento de documentos
│   ├── main.py                    # Entry point del backend
│   └── requirements.txt           # Dependencias Python
│
├── 📁 frontend/                   # Frontend React + Vite (Puerto 5173)
│   ├── 📁 backend-ml/             # Servicio ML (Puerto 8002)
│   │   ├── classifier_service.py  # Clasificador ML
│   │   ├── classifier_model.pkl   # Modelo entrenado
│   │   ├── main.py                # API del servicio ML
│   │   ├── regenerate_model.py    # Script para regenerar modelo
│   │   ├── run_server.py          # Iniciar servicio ML
│   │   └── requirements.txt       # Dependencias ML
│   ├── 📁 src/
│   │   ├── 📁 components/         # Componentes reutilizables
│   │   ├── 📁 pages/
│   │   │   ├── BulkImportPage.tsx # Importación masiva con ML
│   │   │   ├── DocumentsPage.tsx  # Búsqueda avanzada
│   │   │   ├── DashboardPage.tsx  # Panel principal
│   │   │   └── ...
│   │   ├── 📁 services/           # Llamadas a API
│   │   │   ├── api.ts             # Cliente HTTP
│   │   │   ├── auth.ts            # Autenticación
│   │   │   ├── documents.ts       # Gestión de documentos
│   │   │   └── ml.ts              # Servicios ML
│   │   └── 📁 types/              # Tipos TypeScript
│   └── package.json
│
├── 📁 scripts/                    # Scripts de instalación
├── 📁 docs/                       # Documentación
├── .gitignore                     # Exclusiones de Git
└── README.md                      # Este archivo
```

## 🛠️ Stack Tecnológico

### Backend (Puerto 8000)
- **FastAPI 0.104.1**: Framework web moderno y rápido
- **Uvicorn 0.24.0**: Servidor ASGI de alto rendimiento
- **SQLAlchemy**: ORM para base de datos MySQL
- **Pydantic**: Validación de datos y schemas
- **JWT (python-jose)**: Autenticación con tokens
- **PassLib**: Encriptación de contraseñas
- **PyMySQL**: Driver de MySQL

### Servicio ML (Puerto 8002)
- **FastAPI**: API para clasificación de documentos
- **scikit-learn 1.7.2**: Machine Learning
  - **TF-IDF Vectorizer**: Extracción de características de texto
  - **Multinomial Naive Bayes**: Algoritmo de clasificación
- **Joblib**: Persistencia del modelo entrenado
- **NumPy & Pandas**: Procesamiento de datos

### Frontend (Puerto 5173)
- **React 18.2**: Biblioteca de UI
- **TypeScript**: JavaScript tipado
- **Vite 7.1.8**: Build tool ultra rápido
- **Tailwind CSS**: Framework de estilos utilitarios
- **React Router**: Navegación entre páginas
- **Axios**: Cliente HTTP para consumir APIs

### Base de Datos
- **MySQL 8.0+**: Base de datos relacional principal
- Tablas: `users`, `documents`
- Índices optimizados para búsquedas

## 📋 Prerequisitos

- **Python 3.8+** con pip
- **MySQL 8.0+** (local o en contenedor)
- **Node.js 16+** con npm
- **Git** para control de versiones

## ⚡ Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/dario-coronel/clasificador-dms.git
cd clasificador-dms
```

### 2. Configurar Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus configuraciones de MySQL
```

### 3. Configurar Base de Datos MySQL

```sql
-- Crear base de datos
CREATE DATABASE edms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario
CREATE USER 'edms_user'@'localhost' IDENTIFIED BY 'edms_password';
GRANT ALL PRIVILEGES ON edms_db.* TO 'edms_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Configurar Servicio ML

```bash
# Navegar al directorio del servicio ML
cd frontend/backend-ml

# Instalar dependencias
pip install -r requirements.txt

# El modelo ya está pre-entrenado con 12 categorías
# Si necesitas regenerarlo:
python regenerate_model.py
```

### 5. Configurar Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Construir el proyecto (opcional)
npm run build
```

### 6. Ejecutar los 3 Servicios

#### Terminal 1 - Backend (Puerto 8000):
```bash
cd backend
python main.py
```

#### Terminal 2 - Servicio ML (Puerto 8002):
```bash
cd frontend/backend-ml
python run_server.py
```

#### Terminal 3 - Frontend (Puerto 5173):
```bash
cd frontend
npm run dev
```

### 7. Acceder a la Aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Servicio ML API**: http://localhost:8002
- **Swagger UI (Backend)**: http://localhost:8000/docs
- **Swagger UI (ML)**: http://localhost:8002/docs

## 🔧 Configuración

### Variables de Entorno Backend (.env)

```env
# Database
DATABASE_URL=mysql+pymysql://edms_user:edms_password@localhost:3306/edms_db

# Security
SECRET_KEY=tu-clave-secreta-super-segura-cambia-esto-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB

# CORS (si necesitas acceso desde otros orígenes)
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### Configuración del Servicio ML

El servicio ML está configurado para:
- **Puerto**: 8002
- **Modelo**: TF-IDF + Multinomial Naive Bayes
- **12 Categorías**: Contrato, Contrato de Granos, Informe, Factura, Remito, Nota de Crédito, Nota de Débito, Política, Manual, Orden de Compra, Recibo, Otro
- **Entrenamiento automático**: Se actualiza con cada documento aprobado

## 🎯 Uso de la Aplicación

### 1. Registro e Inicio de Sesión

1. Accede a http://localhost:5173
2. Haz clic en "Registrarse" para crear una cuenta
3. Completa el formulario con email y contraseña
4. Inicia sesión con tus credenciales

### 2. Importación Masiva de Documentos

1. Navega a la sección **"Importación Masiva"**
2. Haz clic en "Seleccionar Archivos" o arrastra archivos PDF
3. Los documentos se clasificarán automáticamente con ML
4. Revisa la categoría sugerida para cada documento
5. Modifica la categoría si es necesario haciendo clic en el selector
6. Haz clic en **"Guardar Documentos Aprobados"**
7. ✅ Los documentos se guardan y el modelo ML se entrena automáticamente con estos ejemplos

### 3. Búsqueda Avanzada de Documentos

1. Ve a la sección **"Documentos"**
2. Utiliza los filtros disponibles:
   - **Fecha**: Filtra por rango de fechas
   - **Proveedor**: Busca por nombre de proveedor
   - **CUIT**: Filtra por CUIT del proveedor
   - **Tipo**: Selecciona una de las 12 categorías
3. Los resultados se actualizan automáticamente

### 4. Gestión de Documentos

- **Ver detalles**: Haz clic en cualquier documento para ver información completa
- **Descargar**: Descarga el archivo original
- **Editar metadatos**: Actualiza información del documento
- **Eliminar**: Borra documentos que ya no necesites

## 📚 API Endpoints

### Backend API (Puerto 8000)

#### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión (retorna JWT token)
- `POST /api/v1/auth/register` - Registrar nuevo usuario

#### Usuarios
- `GET /api/v1/users/me` - Obtener perfil del usuario actual
- `PUT /api/v1/users/me` - Actualizar perfil
- `PUT /api/v1/users/me/password` - Cambiar contraseña

#### Documentos
- `POST /api/v1/documents/upload` - Subir un documento
- `POST /api/v1/documents/bulk-upload` - Subir múltiples documentos
- `GET /api/v1/documents/` - Listar documentos (con filtros opcionales)
  - Query params: `fecha_inicio`, `fecha_fin`, `proveedor`, `cuit`, `tipo`
- `GET /api/v1/documents/{id}` - Obtener documento específico
- `PUT /api/v1/documents/{id}` - Actualizar metadatos del documento
- `DELETE /api/v1/documents/{id}` - Eliminar documento

### Servicio ML API (Puerto 8002)

#### Clasificación
- `POST /classify` - Clasificar un documento
  - Body: `{ "text": "contenido del documento" }`
  - Response: `{ "category": "Factura", "confidence": 0.85 }`

- `POST /classify-batch` - Clasificar múltiples documentos
  - Body: `{ "texts": ["texto1", "texto2", ...] }`
  - Response: Lista de categorías y confianzas

#### Entrenamiento
- `POST /train` - Entrenar el modelo con nuevos ejemplos
  - Body: `{ "texts": ["texto1", "texto2"], "labels": ["Factura", "Remito"] }`
  - Response: `{ "message": "Model trained successfully" }`

#### Información
- `GET /categories` - Obtener lista de categorías disponibles
- `GET /health` - Verificar estado del servicio

## � Machine Learning - Clasificador de Documentos

### Arquitectura del Modelo

El clasificador utiliza un pipeline de scikit-learn:

1. **Preprocesamiento de texto**:
   - Conversión a minúsculas
   - Eliminación de caracteres especiales
   - Tokenización

2. **Extracción de características (TF-IDF)**:
   - Term Frequency-Inverse Document Frequency
   - Vectorización de texto a matriz numérica
   - N-gramas: unigramas y bigramas

3. **Clasificación (Multinomial Naive Bayes)**:
   - Algoritmo probabilístico
   - Rápido y eficiente para clasificación de texto
   - Buena precisión con datasets pequeños

### Categorías Soportadas (12 tipos)

1. **Contrato**: Contratos generales
2. **Contrato de Granos**: Contratos específicos del sector agrícola
3. **Informe**: Informes técnicos y reportes
4. **Factura**: Facturas de compra/venta
5. **Remito**: Remitos de entrega
6. **Nota de Crédito**: Notas de crédito
7. **Nota de Débito**: Notas de débito
8. **Política**: Políticas empresariales
9. **Manual**: Manuales de usuario o procedimientos
10. **Orden de Compra**: Órdenes de compra
11. **Recibo**: Recibos de pago
12. **Otro**: Documentos no clasificables en las categorías anteriores

### Entrenamiento Continuo

El sistema implementa **aprendizaje continuo**:
- ✅ Cuando subes documentos en "Importación Masiva" y los apruebas
- ✅ El modelo se entrena automáticamente con estos ejemplos reales
- ✅ Mejora progresivamente con el uso
- ✅ Se adapta al vocabulario específico de tu negocio

### Regenerar el Modelo

Si necesitas reiniciar el modelo:

```bash
cd frontend/backend-ml
python regenerate_model.py
```

Esto creará un nuevo modelo con datos de entrenamiento básicos.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest

# Tests con coverage
pytest --cov=app tests/
```

### ML Service Tests

```bash
cd frontend/backend-ml
python test_ml.py
```

Este script prueba:
- Clasificación de documentos de ejemplo
- Precisión del modelo
- Categorías disponibles

## 🚀 Estado del Proyecto

### ✅ Completado

- ✅ Backend FastAPI con autenticación JWT
- ✅ Frontend React + TypeScript con Vite
- ✅ Servicio ML independiente para clasificación
- ✅ Clasificación automática de documentos (12 categorías)
- ✅ Importación masiva de PDFs
- ✅ Búsqueda avanzada con múltiples filtros
- ✅ Entrenamiento automático del modelo con ejemplos reales
- ✅ Interfaz de usuario moderna y responsiva
- ✅ Gestión completa de documentos (CRUD)
- ✅ Sistema de usuarios con registro e inicio de sesión
- ✅ Almacenamiento de archivos en servidor

### 🔄 En Desarrollo

- ⏳ OCR para extracción de texto de imágenes escaneadas
- ⏳ Sistema de permisos y roles de usuario
- ⏳ Notificaciones en tiempo real
- ⏳ Exportación de reportes (PDF, Excel)
- ⏳ Versionado de documentos
- ⏳ Historial de cambios y auditoría
- ⏳ Dockerización completa del proyecto
- ⏳ Tests unitarios y de integración completos

## 🐛 Solución de Problemas

### El servicio ML no inicia

```bash
# Verifica que tienes las dependencias correctas
cd frontend/backend-ml
pip install -r requirements.txt

# Regenera el modelo si hay problemas de compatibilidad
python regenerate_model.py

# Inicia el servidor
python run_server.py
```

### Error de conexión a MySQL

1. Verifica que MySQL esté corriendo
2. Comprueba las credenciales en `backend/.env`
3. Asegúrate de que la base de datos existe:
```sql
SHOW DATABASES;
```

### El frontend no conecta con el backend

1. Verifica que los 3 servicios estén corriendo:
   - Backend en puerto 8000
   - ML en puerto 8002
   - Frontend en puerto 5173
2. Revisa la consola del navegador para errores CORS
3. Verifica la configuración de URLs en `frontend/src/services/api.ts`

### Modelo ML clasifica incorrectamente

El modelo mejora con el uso:
1. Sube documentos reales en "Importación Masiva"
2. Corrige las categorías incorrectas
3. Guarda los documentos aprobados
4. El modelo se entrenará automáticamente con estos ejemplos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres colaborar:

1. Fork el proyecto
2. Crea una rama para tu feature:
   ```bash
   git checkout -b feature/NuevaFuncionalidad
   ```
3. Commit tus cambios:
   ```bash
   git commit -m 'Añade nueva funcionalidad X'
   ```
4. Push a la rama:
   ```bash
   git push origin feature/NuevaFuncionalidad
   ```
5. Abre un Pull Request describiendo tus cambios

### Áreas donde puedes contribuir

- 🎨 Mejoras en la interfaz de usuario
- 🤖 Optimización del modelo ML
- 📝 Documentación y tutoriales
- 🧪 Tests unitarios y de integración
- 🐛 Corrección de bugs
- ✨ Nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Dario Coronel** - *Desarrollo inicial* - [@dario-coronel](https://github.com/dario-coronel)

## 🆘 Soporte

¿Tienes problemas o preguntas? 

- 📧 Abre un [issue](https://github.com/dario-coronel/clasificador-dms/issues)
- 💬 Revisa la documentación en la carpeta `docs/`
- 📖 Consulta los ejemplos en `frontend/backend-ml/test_documents/`

## 🙏 Agradecimientos

- Gracias a la comunidad de FastAPI por su excelente framework
- Scikit-learn por las herramientas de Machine Learning
- React y Vite por facilitar el desarrollo del frontend
- Todos los contribuidores que hacen posible este proyecto

---

**¡Construyamos el mejor sistema de gestión documental inteligente juntos! 📄🤖✨**

---

### 📊 Estadísticas del Proyecto

- **Lenguajes**: Python, TypeScript/JavaScript
- **Frameworks**: FastAPI, React
- **ML**: scikit-learn (TF-IDF + Naive Bayes)
- **Base de datos**: MySQL
- **Categorías de documentos**: 12
- **Servicios**: 3 (Backend, Frontend, ML)

### 🔗 Links Útiles

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [React + TypeScript](https://react-typescript-cheatsheet.netlify.app/)
- [scikit-learn Docs](https://scikit-learn.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Última actualización**: Octubre 2025