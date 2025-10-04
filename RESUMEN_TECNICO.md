# 🎓 PROYECTO EDMS - RESUMEN TÉCNICO

## 📋 Información General

**Nombre**: Sistema de Gestión Electrónica de Documentos con Clasificación ML
**Fecha**: Octubre 2025
**Tecnologías**: React + FastAPI + Machine Learning

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│                   http://localhost:3000                     │
│  ┌────────────┬──────────────┬──────────────────────────┐  │
│  │ Dashboard  │  Documentos  │  Importación Masiva      │  │
│  │  Perfil    │    Upload    │       Ayuda              │  │
│  └────────────┴──────────────┴──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 BACKEND ML (FastAPI)                        │
│                   http://localhost:8001                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OCR Service       │  Classifier Service             │  │
│  │  - PDF extraction  │  - TF-IDF Vectorizer            │  │
│  │  - Text parsing    │  - Naive Bayes Classifier       │  │
│  │                    │  - Keyword extraction           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Stack Tecnológico

### Frontend
- **Framework**: React 18.2 + TypeScript 5.2
- **Build Tool**: Vite 7.1.8
- **Estilos**: Tailwind CSS 3.3.6
- **Routing**: React Router DOM 6.8
- **HTTP Client**: Axios 1.6.0
- **State Management**: TanStack React Query 4.36.1
- **Icons**: Lucide React 0.294.0

### Backend ML
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **OCR**: PyPDF2 3.0.1 (Tesseract opcional)
- **ML Library**: scikit-learn 1.3.2
- **Data Processing**: 
  - NumPy 1.26.4
  - Pandas 2.1.3
- **Model Persistence**: joblib 1.3.2
- **Python Version**: 3.12.3

---

## 🧠 Machine Learning

### Algoritmo de Clasificación
**TF-IDF + Multinomial Naive Bayes**

#### ¿Por qué TF-IDF?
- **TF (Term Frequency)**: Mide la frecuencia de términos en un documento
- **IDF (Inverse Document Frequency)**: Penaliza términos muy comunes
- Convierte texto a vectores numéricos
- Captura la importancia de las palabras en el contexto

#### ¿Por qué Naive Bayes?
- Rápido para entrenamiento e inferencia
- Funciona bien con datos de alta dimensionalidad (texto)
- Robusto con datasets pequeños
- Probabilidades interpretables

### Pipeline de Procesamiento

```python
# 1. Preprocesamiento
texto_limpio = preprocessor(texto_raw)
# - Convertir a minúsculas
# - Eliminar caracteres especiales
# - Normalizar espacios

# 2. Vectorización
vector = tfidf_vectorizer.transform([texto_limpio])
# - Crear matriz TF-IDF
# - N-gramas: unigrams y bigrams
# - Max features: 5000

# 3. Clasificación
categoria, confianza = classifier.predict_proba(vector)
# - Predecir categoría más probable
# - Calcular probabilidades para todas las categorías

# 4. Extracción de Keywords
keywords = tfidf_vectorizer.get_feature_names_out()
scores = vector.toarray()[0]
top_keywords = sorted(zip(keywords, scores))[-10:]
```

### Categorías Soportadas

| Categoría | Descripción | Ejemplos |
|-----------|-------------|----------|
| 📝 Contrato | Acuerdos legales | Arrendamiento, compraventa, trabajo |
| 📊 Informe | Reportes y análisis | Ventas, financiero, trimestral |
| 🧾 Factura | Documentos fiscales | Facturas, recibos, comprobantes |
| 📋 Política | Normas y políticas | Privacidad, seguridad, reglamentos |
| 📖 Manual | Guías y manuales | Usuario, procedimientos, técnico |
| 📄 Otro | Documentos diversos | No clasificables en anteriores |

### Métricas del Modelo

```python
# Ejemplo con dataset de entrenamiento básico
Precisión estimada: ~65-75% (modelo básico)
# Mejora con más datos: ~85-95% (con entrenamiento adicional)

# Confianza típica:
- Alta (>80%): Clasificación muy probable
- Media (50-80%): Clasificación moderada
- Baja (<50%): Requiere revisión manual
```

---

## 🔌 API Endpoints

### Backend ML (Puerto 8001)

#### 1. GET `/`
**Descripción**: Información de la API
**Respuesta**:
```json
{
  "name": "EDMS ML API (Lite)",
  "version": "1.0.0-lite",
  "endpoints": { ... }
}
```

#### 2. POST `/ocr`
**Descripción**: Extrae texto de un archivo
**Request**: `multipart/form-data` con archivo
**Respuesta**:
```json
{
  "text": "Texto extraído...",
  "success": true,
  "message": "Texto extraído exitosamente"
}
```

#### 3. POST `/classify`
**Descripción**: Clasifica un texto
**Request**:
```json
{
  "text": "Texto a clasificar..."
}
```
**Respuesta**:
```json
{
  "category": "Contrato",
  "confidence": 0.85,
  "all_probabilities": {
    "Contrato": 0.85,
    "Informe": 0.10,
    ...
  },
  "keywords": ["contrato", "partes", "cláusula", ...],
  "success": true,
  "message": "Documento clasificado exitosamente"
}
```

#### 4. POST `/process`
**Descripción**: OCR + Clasificación en una sola llamada
**Request**: `multipart/form-data` con archivo
**Respuesta**: Combinación de OCR + Clasificación

#### 5. POST `/bulk-process`
**Descripción**: Procesa múltiples archivos
**Request**: `multipart/form-data` con múltiples archivos
**Respuesta**:
```json
{
  "total_files": 10,
  "processed": 9,
  "failed": 1,
  "results": [...]
}
```

#### 6. POST `/train`
**Descripción**: Entrena el modelo con nuevos datos
**Request**:
```json
{
  "texts": ["Texto 1", "Texto 2", ...],
  "labels": ["Contrato", "Informe", ...]
}
```
**Respuesta**:
```json
{
  "success": true,
  "message": "Modelo entrenado y guardado exitosamente",
  "trained_samples": 10
}
```

---

## 📁 Estructura del Proyecto

```
Clasificador-DMS/
│
├── frontend/                    # Aplicación React
│   ├── src/
│   │   ├── components/         # Componentes reutilizables
│   │   │   ├── Button.tsx      # Componente de botón
│   │   │   ├── Input.tsx       # Componente de input
│   │   │   ├── Card.tsx        # Componente de tarjeta
│   │   │   ├── Layout.tsx      # Layout principal
│   │   │   └── ToastProvider.tsx # Sistema de notificaciones
│   │   │
│   │   ├── pages/              # Páginas de la aplicación
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── DocumentsPage.tsx
│   │   │   ├── DocumentDetailPage.tsx
│   │   │   ├── UploadPage.tsx
│   │   │   ├── BulkImportPage.tsx  # NUEVA: Importación masiva
│   │   │   ├── ProfilePage.tsx
│   │   │   ├── HelpPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   │
│   │   ├── services/           # Servicios de API
│   │   │   ├── api.ts          # Cliente Axios base
│   │   │   ├── documents.ts    # API de documentos
│   │   │   └── ml.ts           # NUEVO: API ML
│   │   │
│   │   ├── types/              # Definiciones TypeScript
│   │   ├── hooks/              # Custom hooks
│   │   ├── App.tsx             # Componente raíz
│   │   └── main.tsx            # Punto de entrada
│   │
│   ├── backend-ml/             # Servicio ML
│   │   ├── main.py             # API FastAPI (versión completa)
│   │   ├── main_lite.py        # API FastAPI (sin Tesseract)
│   │   ├── run_server.py       # Script de inicio
│   │   ├── ocr_service.py      # Servicio OCR completo
│   │   ├── ocr_service_lite.py # Servicio OCR sin Tesseract
│   │   ├── classifier_service.py # Clasificador ML
│   │   ├── requirements.txt    # Dependencias Python
│   │   ├── install.bat         # Instalador (con Tesseract)
│   │   ├── install_lite.bat    # Instalador (sin Tesseract)
│   │   ├── start_lite.bat      # Script de inicio
│   │   ├── test_ml.py          # Tests del modelo
│   │   ├── README.md           # Documentación
│   │   │
│   │   ├── test_documents/     # Documentos de prueba
│   │   │   ├── contrato_arrendamiento.txt
│   │   │   ├── informe_ventas.txt
│   │   │   ├── factura_2025.txt
│   │   │   └── politica_privacidad.txt
│   │   │
│   │   ├── temp_uploads/       # Archivos temporales
│   │   └── classifier_model.pkl # Modelo entrenado
│   │
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── GUIA_USO.md                 # Guía de usuario
└── RESUMEN_TECNICO.md          # Este archivo
```

---

## 🎨 Componentes del Frontend

### Componentes Reutilizables

#### Button.tsx
```typescript
interface ButtonProps {
  variant: 'primary' | 'outline' | 'danger';
  disabled?: boolean;
  className?: string;
}
```
- Tres variantes de estilo
- Estados disabled
- Clases personalizables

#### Input.tsx
```typescript
interface InputProps {
  label?: string;
  error?: string;
  type?: string;
}
```
- Label integrado
- Mensajes de error
- Tipos múltiples (text, email, password)

#### Card.tsx
```typescript
interface CardProps {
  children: React.ReactNode;
  className?: string;
}
```
- Contenedor con sombra y bordes
- Padding consistente

#### ToastProvider.tsx
```typescript
function showToast(message: string, type: 'success' | 'error' | 'info')
```
- Sistema de notificaciones
- Auto-dismiss en 3 segundos
- Animaciones suaves

### Layout Principal

#### Sidebar (w-72)
- Navegación principal
- Iconos con Lucide React
- Divisores visuales
- Estado activo resaltado
- Totalmente accesible (ARIA)

#### Header
- Barra de búsqueda
- Información del usuario
- Altura fija (h-20)

---

## 🔐 Seguridad

### Consideraciones Actuales
⚠️ **Desarrollo**: Autenticación deshabilitada temporalmente
- CORS habilitado para todos los orígenes (desarrollo)
- Sin validación de tokens JWT
- Sin límite de tasa de solicitudes

### Para Producción (Pendiente)
- [ ] Habilitar autenticación JWT
- [ ] Configurar CORS restrictivo
- [ ] Implementar rate limiting
- [ ] Validación de entrada robusta
- [ ] Escaneo de archivos por virus
- [ ] Cifrado de datos sensibles
- [ ] HTTPS obligatorio

---

## 📊 Rendimiento

### Tiempos de Respuesta (Estimados)

| Operación | Tiempo | Notas |
|-----------|--------|-------|
| Extracción de texto (TXT) | <100ms | Lectura directa |
| Extracción de texto (PDF) | 200-500ms | Depende del tamaño |
| Clasificación ML | 50-150ms | Modelo en memoria |
| Proceso completo (1 archivo) | 300-700ms | OCR + clasificación |
| Proceso masivo (10 archivos) | 3-7s | Secuencial |

### Optimizaciones Futuras
- [ ] Procesamiento paralelo de archivos
- [ ] Cache de resultados OCR
- [ ] Modelo ML más ligero
- [ ] Compresión de respuestas
- [ ] CDN para assets estáticos

---

## 🧪 Testing

### Frontend
```bash
# Ejecutar linter
npm run lint

# Build de producción
npm run build
```

### Backend ML
```bash
# Test de módulos
python test_ml.py

# Test de endpoints
# Usar http://localhost:8001/docs (Swagger UI)
```

### Documentos de Prueba
Archivos listos en `backend-ml/test_documents/`:
- 4 archivos de ejemplo
- Cubren 4 de 6 categorías
- Formato de texto plano

---

## 🚀 Despliegue

### Desarrollo Local
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend ML
cd frontend/backend-ml
pip install -r requirements.txt
python run_server.py
```

### Producción (Pendiente)
- [ ] Dockerizar aplicaciones
- [ ] Configurar nginx/Apache
- [ ] Base de datos PostgreSQL
- [ ] Redis para cache
- [ ] Logs centralizados
- [ ] Monitoreo (Prometheus/Grafana)

---

## 📈 Mejoras Futuras

### Corto Plazo (1-2 semanas)
- [ ] Instalar Tesseract OCR completo
- [ ] Entrenar modelo con más ejemplos
- [ ] Agregar más categorías personalizadas
- [ ] Integrar con backend principal (MySQL)
- [ ] Guardar documentos clasificados en BD

### Mediano Plazo (1-2 meses)
- [ ] Procesamiento asíncrono (Celery)
- [ ] Modelos ML más avanzados (BERT, transformers)
- [ ] Reconocimiento de entidades (NER)
- [ ] Análisis de sentimiento
- [ ] Detección automática de idioma
- [ ] Resumen automático de documentos

### Largo Plazo (3-6 meses)
- [ ] Búsqueda semántica con embeddings
- [ ] Clustering automático de documentos
- [ ] Sistema de recomendaciones
- [ ] Integración con servicios cloud (AWS S3, Google Cloud Storage)
- [ ] API pública con documentación completa
- [ ] Dashboard de analytics

---

## 📚 Recursos y Referencias

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [scikit-learn Docs](https://scikit-learn.org/)
- [React Docs](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

### Tutoriales Utilizados
- Text Classification with scikit-learn
- FastAPI + React Integration
- TF-IDF for Document Classification

### Papers y Artículos
- "Naive Bayes Text Classification"
- "TF-IDF Feature Extraction"

---

## 👥 Créditos

**Desarrollado con**:
- GitHub Copilot
- VS Code
- Python 3.12
- Node.js 20.16

**Fecha de creación**: Octubre 2025

---

## 📝 Notas Técnicas

### Limitaciones Conocidas
1. **Node.js 20.16.0**: Vite requiere 20.19+, pero funciona con advertencia
2. **Modelo ML básico**: Precisión limitada sin entrenamiento adicional
3. **OCR sin imágenes**: Versión lite no procesa imágenes escaneadas
4. **Sin autenticación**: Deshabilitada temporalmente para desarrollo
5. **Procesamiento secuencial**: No hay paralelización en bulk-process

### Decisiones de Diseño
- **TF-IDF + Naive Bayes**: Balance entre rendimiento y precisión
- **FastAPI**: Velocidad y documentación automática
- **React + Vite**: Desarrollo rápido y HMR
- **Tailwind CSS**: Estilos utilitarios y responsive
- **TypeScript**: Seguridad de tipos
- **Versión Lite**: Funcionamiento sin Tesseract para facilitar setup

---

**Fin del Resumen Técnico**
