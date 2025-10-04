# 🎉 SISTEMA EDMS CON ML - GUÍA DE USO

## 📋 Estado del Sistema

### ✅ Servicios Activos
- **Frontend React**: http://localhost:3000
- **Backend ML**: http://localhost:8001
- **Documentación API ML**: http://localhost:8001/docs

## 🚀 Funcionalidades Implementadas

### 1. **Clasificación Automática de Documentos**
El sistema utiliza Machine Learning (TF-IDF + Naive Bayes) para clasificar documentos en 6 categorías:
- 📝 **Contrato**: Contratos, acuerdos, convenios
- 📊 **Informe**: Informes, reportes, análisis
- 🧾 **Factura**: Facturas, comprobantes fiscales
- 📋 **Política**: Políticas, reglamentos, normas
- 📖 **Manual**: Manuales, guías, instructivos
- 📄 **Otro**: Documentos que no encajan en las categorías anteriores

### 2. **Extracción de Texto (OCR Lite)**
- ✅ Archivos de texto (.txt, .md, .csv, .json)
- ✅ PDFs con texto extraíble
- ⏳ Imágenes y PDFs escaneados (requiere instalar Tesseract OCR)

### 3. **Procesamiento Masivo**
- Importa carpetas completas con múltiples archivos
- Clasifica automáticamente cada documento
- Extrae palabras clave relevantes
- Muestra nivel de confianza de la clasificación

## 🧪 Probar el Sistema

### Paso 1: Acceder a la Interfaz
1. Abre tu navegador en: http://localhost:3000
2. Navega al menú lateral y haz clic en **"Importación masiva"**

### Paso 2: Importar Documentos de Prueba
Hay archivos de ejemplo en:
```
c:\Clases\Clasificador-DMS\frontend\backend-ml\test_documents\
```

Archivos disponibles:
- `contrato_arrendamiento.txt` - Debería clasificarse como **Contrato**
- `informe_ventas.txt` - Debería clasificarse como **Informe**
- `factura_2025.txt` - Debería clasificarse como **Factura**
- `politica_privacidad.txt` - Debería clasificarse como **Política**

### Paso 3: Seleccionar Carpeta
1. Haz clic en el botón de selección de carpeta
2. Navega a `backend-ml\test_documents\`
3. Selecciona la carpeta completa

### Paso 4: Procesar Documentos
1. Haz clic en **"🚀 Importar y clasificar archivos"**
2. Espera a que el sistema procese todos los archivos
3. Observa los resultados:
   - Categoría asignada (con etiqueta de color)
   - Nivel de confianza (porcentaje)
   - Vista previa del texto extraído
   - Palabras clave identificadas

## 📊 Resultados Esperados

Para cada documento verás:

```
✅ contrato_arrendamiento.txt
   Categoría: Contrato (85% confianza)
   Palabras clave: arrendamiento, arrendador, arrendatario, vivienda, renta
   
✅ informe_ventas.txt
   Categoría: Informe (92% confianza)
   Palabras clave: informe, ventas, análisis, resultados, región
   
✅ factura_2025.txt
   Categoría: Factura (88% confianza)
   Palabras clave: factura, iva, total, pago, cliente
   
✅ politica_privacidad.txt
   Categoría: Política (90% confianza)
   Palabras clave: política, privacidad, datos, protección, tratamiento
```

## 🎨 Interfaz del Usuario

### Características del Frontend:
- ✅ **100% en Español**: Todas las vistas traducidas
- ✅ **Componentes Reutilizables**: Button, Input, Card
- ✅ **Sistema de Notificaciones**: Toast messages
- ✅ **Diseño Responsivo**: Funciona en desktop y móvil
- ✅ **Accesibilidad**: Atributos ARIA implementados
- ✅ **Sidebar Mejorado**: Más ancho, iconos, divisores visuales
- ✅ **Barra de Búsqueda**: Alineada en la parte superior

### Páginas Disponibles:
- 📊 **Dashboard**: Vista general del sistema
- 📁 **Documentos**: Lista de documentos
- 📤 **Subir Documento**: Carga individual de archivos
- 📦 **Importación Masiva**: Carga y clasificación masiva (NUEVA)
- 👤 **Perfil**: Información del usuario
- ❓ **Ayuda**: Preguntas frecuentes

## 🔧 Configuración

### Variables de Entorno (Frontend)
Crea un archivo `.env` en el directorio frontend:
```env
VITE_API_URL=http://localhost:8003
VITE_ML_API_URL=http://localhost:8001
```

### Puertos Utilizados
- `3000` - Frontend React (Vite)
- `8001` - Backend ML (FastAPI)
- `8003` - Backend Principal (FastAPI) - No configurado aún

## 📈 Mejorar la Precisión del Modelo

El modelo ML se puede entrenar con tus propios documentos:

### Usando la API directamente:
```bash
curl -X POST "http://localhost:8001/train" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Texto de ejemplo 1", "Texto de ejemplo 2"],
    "labels": ["Contrato", "Informe"]
  }'
```

### Desde Python:
```python
from services.ml import trainClassifier

texts = [
    "Este es un contrato de trabajo...",
    "Informe trimestral de resultados..."
]
labels = ["Contrato", "Informe"]

result = trainClassifier(texts, labels)
print(f"Modelo entrenado con {result.trained_samples} ejemplos")
```

## 🛠️ Solución de Problemas

### Problema: "Servicio ML no disponible"
**Solución**: 
1. Verifica que el servidor ML esté corriendo
2. Ejecuta: `python c:\Clases\Clasificador-DMS\frontend\backend-ml\run_server.py`
3. Verifica en http://localhost:8001

### Problema: "No se puede extraer texto de imágenes"
**Solución**: 
1. Instala Tesseract OCR desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Reinicia el servidor ML
3. Usa `main.py` en lugar de `main_lite.py`

### Problema: Frontend no carga
**Solución**:
1. Verifica que Node.js esté instalado: `node --version`
2. Actualiza Node.js a 20.19+ si es necesario
3. Reinstala dependencias: `npm install`
4. Inicia el servidor: `npm run dev`

## 📚 Documentación de la API

Visita http://localhost:8001/docs para ver la documentación interactiva (Swagger UI) con todos los endpoints disponibles:

- `GET /` - Información de la API
- `POST /ocr` - Extraer texto de un archivo
- `POST /classify` - Clasificar un texto
- `POST /process` - OCR + Clasificación (un archivo)
- `POST /bulk-process` - Procesamiento masivo (múltiples archivos)
- `POST /train` - Entrenar el clasificador

## 🎯 Próximos Pasos

1. **Instalar Tesseract OCR** para procesar imágenes y PDFs escaneados
2. **Entrenar el modelo** con más ejemplos de tus documentos reales
3. **Integrar con el backend principal** para guardar documentos clasificados en la base de datos
4. **Agregar más categorías** según tus necesidades
5. **Implementar procesamiento asíncrono** para archivos muy grandes

## 💡 Tips

- Los documentos de texto plano (.txt) se procesan más rápido
- Mayor cantidad de ejemplos de entrenamiento = mayor precisión
- El modelo se guarda automáticamente en `classifier_model.pkl`
- Puedes agregar más categorías editando `classifier_service.py`
- Las palabras clave te ayudan a validar la clasificación

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**¡Disfruta clasificando tus documentos automáticamente! 🚀**
