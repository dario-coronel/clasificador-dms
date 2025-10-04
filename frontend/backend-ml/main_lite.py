"""
API FastAPI para procesamiento de documentos con OCR y clasificación ML
Versión Completa: Con OCR de imágenes usando Tesseract
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import shutil
from pathlib import Path
import uuid

from ocr_service import ocr_service
from classifier_service import classifier

app = FastAPI(
    title="EDMS ML API",
    description="API para OCR y clasificación automática de documentos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio temporal para archivos
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Modelos Pydantic
class OCRResponse(BaseModel):
    text: str
    success: bool = True
    message: str = "Texto extraído exitosamente"


class ClassificationRequest(BaseModel):
    text: str


class ClassificationResponse(BaseModel):
    category: str
    confidence: float
    all_probabilities: Dict[str, float]
    keywords: List[str]
    success: bool = True
    message: str = "Documento clasificado exitosamente"


class ProcessedDocument(BaseModel):
    filename: str
    text: Optional[str] = None
    text_preview: Optional[str] = None
    full_text_length: int = 0
    category: Optional[str] = None
    confidence: Optional[float] = None
    all_probabilities: Optional[Dict[str, float]] = None
    keywords: Optional[List[str]] = None
    success: bool = True
    error: Optional[str] = None


class BulkProcessResult(BaseModel):
    total_files: int
    processed: int
    failed: int
    results: List[ProcessedDocument]


class TrainingRequest(BaseModel):
    texts: List[str]
    labels: List[str]


class TrainingResponse(BaseModel):
    success: bool
    message: str
    trained_samples: int


# Rutas
@app.get("/")
async def root():
    """Información de la API"""
    return {
        "name": "EDMS ML API (Lite)",
        "version": "1.0.0-lite",
        "description": "API para clasificación automática de documentos",
        "note": "Esta versión NO incluye OCR de imágenes. Solo procesa texto y PDFs.",
        "tesseract_required": "Para OCR de imágenes, instala Tesseract OCR",
        "endpoints": {
            "GET /": "Esta información",
            "POST /ocr": "Extraer texto de archivo (solo TXT y PDF)",
            "POST /classify": "Clasificar texto en categorías",
            "POST /process": "Procesar archivo completo (extracción + clasificación)",
            "POST /bulk-process": "Procesar múltiples archivos",
            "POST /train": "Entrenar el clasificador con nuevos datos"
        },
        "docs": "/docs"
    }


@app.post("/ocr", response_model=OCRResponse)
async def extract_text(file: UploadFile = File(...)):
    """
    Extrae texto de un documento usando OCR
    
    Soporta:
    - Imágenes (JPG, PNG, GIF)
    - PDFs (con o sin texto)
    - Archivos de texto
    """
    temp_path = None
    try:
        # Guardar archivo temporal
        file_ext = os.path.splitext(file.filename)[1]
        temp_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_ext}"
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determinar tipo MIME
        mime_type = file.content_type or "application/octet-stream"
        
        # Extraer texto
        try:
            text = ocr_service.extract_text_from_file(str(temp_path), mime_type)
            
            return OCRResponse(
                text=text,
                success=True,
                message=f"Texto extraído exitosamente de {file.filename}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al extraer texto: {str(e)}"
            )
    
    finally:
        # Limpiar archivo temporal
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: ClassificationRequest):
    """
    Clasifica un texto en categorías predefinidas.
    
    Categorías:
    - Contrato
    - Informe
    - Factura
    - Política
    - Manual
    - Otro
    """
    try:
        category, confidence, all_probs = classifier.classify_document(request.text)
        keywords = classifier.extract_keywords(request.text)
        
        return ClassificationResponse(
            category=category,
            confidence=confidence,
            all_probabilities=all_probs,
            keywords=keywords,
            success=True,
            message=f"Documento clasificado como '{category}' con confianza {confidence:.2%}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al clasificar documento: {str(e)}"
        )


@app.post("/process", response_model=ProcessedDocument)
async def process_document(file: UploadFile = File(...)):
    """
    Procesa un documento completo: extrae texto y lo clasifica.
    
    Este endpoint combina OCR + Clasificación en una sola llamada.
    """
    temp_path = None
    try:
        # Guardar archivo temporal
        file_ext = os.path.splitext(file.filename)[1]
        temp_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_ext}"
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determinar tipo MIME
        mime_type = file.content_type or "application/octet-stream"
        
        # Extraer texto
        try:
            text = ocr_service.extract_text_from_file(str(temp_path), mime_type)
        except Exception as e:
            return ProcessedDocument(
                filename=file.filename,
                success=False,
                error=f"Error al extraer texto: {str(e)}"
            )
        
        if not text.strip():
            return ProcessedDocument(
                filename=file.filename,
                text="",
                full_text_length=0,
                success=False,
                error="No se pudo extraer texto del archivo"
            )
        
        # Clasificar
        try:
            category, confidence, all_probs = classifier.classify_document(text)
            keywords = classifier.extract_keywords(text)
            
            # Crear preview del texto (primeros 200 caracteres)
            text_preview = text[:200] + "..." if len(text) > 200 else text
            
            return ProcessedDocument(
                filename=file.filename,
                text=text,
                text_preview=text_preview,
                full_text_length=len(text),
                category=category,
                confidence=confidence,
                all_probabilities=all_probs,
                keywords=keywords,
                success=True
            )
        
        except Exception as e:
            return ProcessedDocument(
                filename=file.filename,
                text=text,
                text_preview=text[:200],
                full_text_length=len(text),
                success=False,
                error=f"Error al clasificar: {str(e)}"
            )
    
    finally:
        # Limpiar archivo temporal
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/bulk-process", response_model=BulkProcessResult)
async def bulk_process_documents(files: List[UploadFile] = File(...)):
    """
    Procesa múltiples documentos en lote.
    
    Retorna resultados para cada archivo, incluyendo éxitos y fallos.
    """
    results = []
    processed_count = 0
    failed_count = 0
    
    for file in files:
        temp_path = None
        try:
            # Guardar archivo temporal
            file_ext = os.path.splitext(file.filename)[1]
            temp_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_ext}"
            
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Determinar tipo MIME
            mime_type = file.content_type or "application/octet-stream"
            
            # Extraer texto
            try:
                text = ocr_service.extract_text_from_file(str(temp_path), mime_type)
            except Exception as e:
                results.append(ProcessedDocument(
                    filename=file.filename,
                    success=False,
                    error=f"Error al extraer texto: {str(e)}"
                ))
                failed_count += 1
                continue
            
            if not text.strip():
                results.append(ProcessedDocument(
                    filename=file.filename,
                    text="",
                    full_text_length=0,
                    success=False,
                    error="No se pudo extraer texto del archivo"
                ))
                failed_count += 1
                continue
            
            # Clasificar
            try:
                category, confidence, all_probs = classifier.classify_document(text)
                keywords = classifier.extract_keywords(text)
                
                text_preview = text[:200] + "..." if len(text) > 200 else text
                
                results.append(ProcessedDocument(
                    filename=file.filename,
                    text_preview=text_preview,
                    full_text_length=len(text),
                    category=category,
                    confidence=confidence,
                    all_probabilities=all_probs,
                    keywords=keywords,
                    success=True
                ))
                processed_count += 1
            
            except Exception as e:
                results.append(ProcessedDocument(
                    filename=file.filename,
                    text_preview=text[:200],
                    full_text_length=len(text),
                    success=False,
                    error=f"Error al clasificar: {str(e)}"
                ))
                failed_count += 1
        
        finally:
            # Limpiar archivo temporal
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    
    return BulkProcessResult(
        total_files=len(files),
        processed=processed_count,
        failed=failed_count,
        results=results
    )


@app.post("/train", response_model=TrainingResponse)
async def train_classifier(request: TrainingRequest):
    """
    Entrena el clasificador con nuevos datos.
    
    Proporciona textos de ejemplo y sus categorías correspondientes
    para mejorar la precisión del modelo.
    """
    try:
        if len(request.texts) != len(request.labels):
            raise HTTPException(
                status_code=400,
                detail="El número de textos debe coincidir con el número de etiquetas"
            )
        
        if len(request.texts) == 0:
            raise HTTPException(
                status_code=400,
                detail="Debe proporcionar al menos un ejemplo de entrenamiento"
            )
        
        # Entrenar
        classifier.train_with_new_data(request.texts, request.labels)
        
        return TrainingResponse(
            success=True,
            message="Modelo entrenado y guardado exitosamente",
            trained_samples=len(request.texts)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al entrenar modelo: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("""
    ====================================
    EDMS ML API - Iniciando...
    ====================================
    
    OCR completo disponible con Tesseract.
    Soporta imágenes, PDFs y archivos de texto.
    
    Servidor: http://localhost:8001
    Documentación: http://localhost:8001/docs
    ====================================
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
