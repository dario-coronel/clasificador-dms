# EDMS ML Backend

Backend de Machine Learning para el Sistema de Gestión Electrónica de Documentos (EDMS).

## Características

- **OCR (Reconocimiento Óptico de Caracteres)**: Extracción de texto de imágenes y PDFs
- **Clasificación Automática**: Clasifica documentos en categorías usando Machine Learning
- **Procesamiento Masivo**: Procesa múltiples documentos simultáneamente
- **Extracción de Palabras Clave**: Identifica términos relevantes en los documentos

## Requisitos

- Python 3.8+
- Tesseract OCR (para OCR de imágenes)

### Instalar Tesseract OCR

#### Windows
1. Descargar el instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar en `C:\Program Files\Tesseract-OCR\`
3. Agregar al PATH del sistema

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

#### macOS
```bash
brew install tesseract tesseract-lang
```

## Instalación

1. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar Tesseract (solo Windows):**
Si está instalado en una ruta diferente, editar `ocr_service.py` línea 11:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Uso

### Iniciar el servidor

```bash
python main.py
```

El servidor estará disponible en: `http://localhost:8001`

### Documentación de la API

Una vez iniciado el servidor, acceder a:
- Documentación interactiva (Swagger): `http://localhost:8001/docs`
- Documentación alternativa (ReDoc): `http://localhost:8001/redoc`

## Endpoints

### POST `/ocr`
Extrae texto de un documento usando OCR.

**Parámetros:**
- `file`: Archivo a procesar (imagen, PDF, texto)

**Respuesta:**
```json
{
  "text": "Texto extraído del documento",
  "success": true,
  "message": "Texto extraído exitosamente"
}
```

### POST `/classify`
Clasifica un texto en categorías predefinidas.

**Parámetros:**
- `text`: Texto a clasificar

**Respuesta:**
```json
{
  "category": "Contrato",
  "confidence": 0.85,
  "all_probabilities": {
    "Contrato": 0.85,
    "Informe": 0.10,
    "Factura": 0.03,
    "Política": 0.01,
    "Manual": 0.01,
    "Otro": 0.00
  },
  "keywords": ["contrato", "arrendamiento", "partes", ...],
  "success": true,
  "message": "Documento clasificado exitosamente"
}
```

### POST `/process`
Procesa un documento completo: OCR + Clasificación.

**Parámetros:**
- `file`: Archivo a procesar

**Respuesta:**
```json
{
  "filename": "documento.pdf",
  "text": "Texto extraído...",
  "full_text_length": 1234,
  "category": "Informe",
  "confidence": 0.92,
  "all_probabilities": {...},
  "keywords": [...],
  "success": true,
  "message": "Documento procesado exitosamente"
}
```

### POST `/bulk-process`
Procesa múltiples documentos en lote.

**Parámetros:**
- `files`: Lista de archivos a procesar

**Respuesta:**
```json
{
  "total_files": 10,
  "processed": 9,
  "failed": 1,
  "results": [
    {
      "filename": "doc1.pdf",
      "text": "...",
      "category": "Contrato",
      "confidence": 0.88,
      "keywords": [...],
      "success": true,
      "error": null
    },
    ...
  ]
}
```

### POST `/train`
Entrena el clasificador con nuevos datos.

**Parámetros:**
- `texts`: Lista de textos de documentos
- `labels`: Lista de categorías correspondientes

## Categorías Disponibles

1. **Contrato**: Contratos, acuerdos, convenios
2. **Informe**: Informes, reportes, análisis
3. **Factura**: Facturas, comprobantes fiscales
4. **Política**: Políticas, reglamentos, normas
5. **Manual**: Manuales, guías, instructivos
6. **Otro**: Documentos que no encajan en las categorías anteriores

## Arquitectura

```
backend-ml/
├── main.py                    # FastAPI app principal
├── ocr_service.py            # Servicio de OCR
├── classifier_service.py     # Servicio de clasificación ML
├── requirements.txt          # Dependencias Python
├── temp_uploads/             # Archivos temporales
└── classifier_model.pkl      # Modelo ML entrenado
```

## Personalización

### Agregar nuevas categorías

Editar `classifier_service.py`, línea 16:
```python
self.categories = [
    'Contrato',
    'Informe',
    'Factura',
    'Política',
    'Manual',
    'Tu_Nueva_Categoria',
    'Otro'
]
```

Luego, entrenar el modelo con ejemplos de la nueva categoría usando el endpoint `/train`.

### Mejorar el modelo

1. Recopilar documentos de ejemplo de cada categoría
2. Extraer el texto de cada documento
3. Usar el endpoint `/train` con los textos y categorías
4. El modelo se guardará automáticamente en `classifier_model.pkl`

## Integración con Frontend

El frontend debe enviar archivos a los endpoints de procesamiento:

```typescript
// Ejemplo de integración
const formData = new FormData();
formData.append('file', file);

const response = await fetch('http://localhost:8001/process', {
  method: 'POST',
  body: formData,
});

const result = await response.json();
console.log('Categoría:', result.category);
console.log('Confianza:', result.confidence);
```

## Solución de Problemas

### Error: Tesseract not found
- Verificar que Tesseract OCR esté instalado
- Configurar la ruta correcta en `ocr_service.py`

### Error: No module named 'pytesseract'
```bash
pip install -r requirements.txt
```

### Clasificación incorrecta
- El modelo básico tiene datos limitados
- Entrenar con más ejemplos usando `/train`
- Proporcionar al menos 10-20 ejemplos por categoría

## Mejoras Futuras

- [ ] Soporte para más formatos de archivo (DOCX, XLSX)
- [ ] Modelos de clasificación más avanzados (BERT, transformers)
- [ ] Cache de resultados de OCR
- [ ] Procesamiento asíncrono para archivos grandes
- [ ] Reconocimiento de entidades (NER)
- [ ] Análisis de sentimiento
- [ ] Detección de idioma automática

## Licencia

MIT

## Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio.
