"""
OCR Service - Versión sin Tesseract
Solo procesa archivos de texto y PDFs con texto extraíble.
Para OCR de imágenes, instalar Tesseract OCR.
"""

import os
from typing import Optional
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)


class OCRService:
    """Servicio de extracción de texto sin OCR de imágenes"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.tesseract_available = False
        logger.warning("OCR Service iniciado sin Tesseract. Solo se procesarán archivos de texto y PDFs.")
        self._initialized = True
    
    def extract_text_from_image(self, image_path: str, lang: str = 'spa+eng') -> str:
        """
        Extrae texto de una imagen usando OCR.
        NOTA: Requiere Tesseract OCR instalado.
        """
        raise NotImplementedError(
            "OCR de imágenes no disponible. "
            "Para procesar imágenes, instala Tesseract OCR desde: "
            "https://github.com/UB-Mannheim/tesseract/wiki"
        )
    
    def extract_text_from_pdf(self, pdf_path: str, use_ocr: bool = False) -> str:
        """
        Extrae texto de un PDF.
        Intenta primero extraer texto directamente.
        Si use_ocr=True y hay imágenes, requiere Tesseract.
        """
        try:
            # Intentar extracción directa de texto
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():
                logger.info(f"Texto extraído exitosamente del PDF: {os.path.basename(pdf_path)}")
                return text.strip()
            
            # Si no hay texto y se solicitó OCR
            if use_ocr:
                raise NotImplementedError(
                    "Este PDF parece ser una imagen escaneada. "
                    "Para procesar PDFs escaneados, instala Tesseract OCR desde: "
                    "https://github.com/UB-Mannheim/tesseract/wiki"
                )
            
            logger.warning(f"No se pudo extraer texto del PDF: {os.path.basename(pdf_path)}")
            return ""
            
        except Exception as e:
            logger.error(f"Error al extraer texto del PDF: {str(e)}")
            raise Exception(f"Error al procesar PDF: {str(e)}")
    
    def extract_text_from_file(self, file_path: str, mime_type: Optional[str] = None) -> str:
        """
        Extrae texto de un archivo según su tipo.
        Soporta: TXT, PDF (con texto extraíble)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Determinar tipo de archivo
        ext = os.path.splitext(file_path)[1].lower()
        
        # Archivos de texto plano
        if ext in ['.txt', '.md', '.csv', '.json', '.xml']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                logger.info(f"Texto leído de archivo de texto: {os.path.basename(file_path)}")
                return text
            except UnicodeDecodeError:
                # Intentar con otra codificación
                with open(file_path, 'r', encoding='latin-1') as f:
                    text = f.read()
                logger.info(f"Texto leído (latin-1) de archivo: {os.path.basename(file_path)}")
                return text
        
        # PDFs
        elif ext == '.pdf':
            return self.extract_text_from_pdf(file_path, use_ocr=True)
        
        # Imágenes - requiere Tesseract
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            raise NotImplementedError(
                f"Para procesar imágenes ({ext}), instala Tesseract OCR desde: "
                "https://github.com/UB-Mannheim/tesseract/wiki"
            )
        
        else:
            raise ValueError(f"Tipo de archivo no soportado: {ext}")


# Instancia singleton
ocr_service = OCRService()
