"""
Servicio de OCR para extracción de texto de documentos
"""
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
import io
from typing import Optional
import os

class OCRService:
    def __init__(self):
        # Configurar ruta de tesseract si es necesario (Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text_from_image(self, image_path: str, lang: str = 'spa+eng') -> str:
        """
        Extrae texto de una imagen usando Tesseract OCR
        
        Args:
            image_path: Ruta a la imagen
            lang: Idioma para OCR (por defecto español + inglés)
            
        Returns:
            Texto extraído
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            raise Exception(f"Error al procesar imagen: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str, use_ocr: bool = True) -> str:
        """
        Extrae texto de un PDF. Intenta primero con extracción directa,
        si no funciona, usa OCR.
        
        Args:
            pdf_path: Ruta al archivo PDF
            use_ocr: Si es True, usa OCR cuando no hay texto directo
            
        Returns:
            Texto extraído
        """
        text = ""
        
        try:
            # Intentar extracción directa de texto
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Si no se extrajo texto y use_ocr es True, usar OCR
            if not text.strip() and use_ocr:
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    page_text = pytesseract.image_to_string(image, lang='spa+eng')
                    text += f"--- Página {i+1} ---\n{page_text}\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error al procesar PDF: {str(e)}")
    
    def extract_text_from_file(self, file_path: str, mime_type: str) -> str:
        """
        Extrae texto de un archivo según su tipo MIME
        
        Args:
            file_path: Ruta al archivo
            mime_type: Tipo MIME del archivo
            
        Returns:
            Texto extraído
        """
        if mime_type.startswith('image/'):
            return self.extract_text_from_image(file_path)
        elif mime_type == 'application/pdf':
            return self.extract_text_from_pdf(file_path)
        elif mime_type.startswith('text/'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise Exception(f"Tipo de archivo no soportado para OCR: {mime_type}")

# Singleton
ocr_service = OCRService()
