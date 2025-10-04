"""
Versión simplificada de main.py para depurar problemas de conexión
"""
import os
from fastapi import FastAPI
import uvicorn

# Test básico sin SQLAlchemy
app = FastAPI(title="EDMS API - Debug", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "EDMS API funcionando", "status": "OK"}

@app.get("/test-db")
async def test_database():
    """Probar conexión a la base de datos"""
    try:
        import pymysql
        
        # Configuración desde variables de entorno o valores por defecto
        config = {
            'host': 'localhost',
            'port': 3307,
            'user': 'edms_user',
            'password': 'edms_password123',
            'database': 'edms_db'
        }
        
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Database OK' as status, VERSION() as version")
            result = cursor.fetchone()
            
        connection.close()
        
        return {
            "database_status": "connected",
            "message": result[0],
            "mysql_version": result[1],
            "config": {
                "host": config['host'],
                "port": config['port'],
                "database": config['database'],
                "user": config['user']
            }
        }
        
    except Exception as e:
        return {
            "database_status": "error",
            "error": str(e),
            "config_attempted": {
                "host": "localhost",
                "port": 3307,
                "database": "edms_db",
                "user": "edms_user"
            }
        }

@app.get("/test-sqlalchemy")
async def test_sqlalchemy():
    """Probar SQLAlchemy con la configuración actual"""
    try:
        from sqlalchemy import create_engine, text
        
        # URL de conexión
        DATABASE_URL = "mysql+pymysql://edms_user:edms_password123@localhost:3307/edms_db"
        
        # Crear engine
        engine = create_engine(DATABASE_URL, echo=True)
        
        # Probar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 'SQLAlchemy OK' as status"))
            row = result.fetchone()
            
        return {
            "sqlalchemy_status": "connected",
            "message": row[0],
            "database_url": DATABASE_URL
        }
        
    except Exception as e:
        return {
            "sqlalchemy_status": "error",
            "error": str(e),
            "database_url": "mysql+pymysql://edms_user:***@localhost:3307/edms_db"
        }

if __name__ == "__main__":
    print("🚀 Iniciando EDMS API Debug...")
    print("📋 Endpoints disponibles:")
    print("  - http://localhost:8000/ (Test básico)")
    print("  - http://localhost:8000/test-db (Test PyMySQL)")
    print("  - http://localhost:8000/test-sqlalchemy (Test SQLAlchemy)")
    print("  - http://localhost:8000/docs (Documentación)")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")