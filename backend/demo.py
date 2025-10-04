"""
Versión simplificada de FastAPI para probar sin dependencias complejas
"""
from fastapi import FastAPI
import uvicorn

# Crear aplicación FastAPI simple
app = FastAPI(
    title="EDMS API - Demo",
    version="1.0.0",
    description="Sistema de Gestión Documental - Demostración"
)

@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido al EDMS API!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EDMS API"}

@app.get("/api/info")
async def api_info():
    return {
        "api_name": "EDMS (Electronic Document Management System)",
        "features": [
            "Gestión de documentos",
            "Autenticación JWT",
            "Control de permisos",
            "OCR de texto",
            "Búsqueda avanzada",
            "Versionado de archivos"
        ],
        "stack": {
            "backend": "FastAPI + Python",
            "database": "MySQL",
            "frontend": "React (próximamente)"
        }
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 EDMS API - Demostración")
    print("="*60)
    print("📋 Sistema de Gestión Documental")
    print("🌐 URL: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("💚 Estado: http://localhost:8000/health")
    print("ℹ️  Info API: http://localhost:8000/api/info")
    print("="*60)
    print("🔧 Para configurar MySQL, ve a: docs/database-setup.md")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")