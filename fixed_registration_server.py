"""
Solución temporal para el problema de registro
Vamos a crear un endpoint de registro que funcione
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import pymysql
import os
from datetime import datetime
from typing import Optional

app = FastAPI(title="EDMS Fixed Registration")

# Modelo de usuario simplificado
class UserCreate(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: str

# Configuración de base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'edms_user',
    'password': 'edms_password_2024',
    'database': 'edms_db',
    'port': 3306
}

def hash_password(password: str) -> str:
    """Hash simple de contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """Obtener conexión a la base de datos"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/")
async def root():
    return {"message": "EDMS Fixed Registration API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Endpoint de registro simplificado y funcional"""
    
    print(f"🔍 Processing registration for: {user_data.email}")
    
    try:
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute(
            "SELECT id FROM users WHERE email = %s OR username = %s",
            (user_data.email, user_data.username)
        )
        
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash de la contraseña
        hashed_password = hash_password(user_data.password)
        
        # Insertar nuevo usuario
        now = datetime.now()
        insert_query = """
        INSERT INTO users (email, username, first_name, last_name, password_hash, 
                          phone, department, position, is_active, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            user_data.email,
            user_data.username,
            user_data.first_name,
            user_data.last_name,
            hashed_password,
            user_data.phone,
            user_data.department,
            user_data.position,
            True,  # is_active
            now,
            now
        ))
        
        # Obtener el ID del usuario creado
        user_id = cursor.lastrowid
        
        # Confirmar la transacción
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"✅ User registered successfully with ID: {user_id}")
        
        # Retornar el usuario creado
        return UserResponse(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True,
            created_at=now.isoformat()
        )
        
    except pymysql.Error as e:
        print(f"❌ Database error: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting EDMS Fixed Registration Server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")