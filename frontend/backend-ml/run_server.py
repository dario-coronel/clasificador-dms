"""
Scriptprint("=" * 60)
print("EDMS ML API - Iniciando...")
print("=" * 60)
print()
print("Directorio de trabajo:", os.getcwd())
print()
print("OCR completo disponible con Tesseract.")
print("Soporta imágenes, PDFs y archivos de texto.")
print()
print("Servidor: http://localhost:8001")
print("Documentación: http://localhost:8001/docs")
print("=" * 60)
print()el servidor ML Backend
"""
import sys
import os

# Asegurar que estamos en el directorio correcto
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print("=" * 60)
print("EDMS ML API (Lite) - Iniciando...")
print("=" * 60)
print()
print("Directorio de trabajo:", os.getcwd())
print()
print("NOTA: Esta versión NO incluye OCR de imágenes.")
print("Solo procesa archivos de texto y PDFs con texto extraíble.")
print()
print("Para OCR de imágenes, instala Tesseract OCR:")
print("https://github.com/UB-Mannheim/tesseract/wiki")
print()
print("Servidor: http://localhost:8002")
print("Documentación: http://localhost:8002/docs")
print("=" * 60)
print()

if __name__ == "__main__":
    import uvicorn
    from main import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        log_level="info"
    )
