"""
Servidor de registro ultra simple y robusto
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import pymysql
from datetime import datetime
from typing import Optional
import uvicorn
import traceback

app = FastAPI(title="EDMS Simple Registration", version="1.0.0")

# Modelo de usuario
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
    is_active: bool = True

# Configuración de base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'edms_user',
    'password': 'edms_password_2024',
    'database': 'edms_db',
    'port': 3306,
    'autocommit': True
}

def simple_hash(password: str) -> str:
    """Hash simple de contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
async def root():
    return {"message": "EDMS Simple Registration Server", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "registration"}

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Registro de usuario simplificado"""
    
    print(f"\n🔍 [REGISTER] Processing: {user_data.email}")
    
    conn = None
    cursor = None
    
    try:
        # Conectar a la base de datos
        print("📡 [DB] Connecting to database...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ [DB] Connected successfully")
        
        # Verificar si el usuario ya existe
        print("🔍 [DB] Checking if user exists...")
        cursor.execute(
            "SELECT id FROM users WHERE email = %s OR username = %s",
            (user_data.email, user_data.username)
        )
        
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"⚠️ [DB] User already exists: {user_data.email}")
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash de la contraseña
        print("🔒 [HASH] Hashing password...")
        hashed_password = simple_hash(user_data.password)
        
        # Insertar nuevo usuario
        print("💾 [DB] Inserting new user...")
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
        
        # Obtener el ID del usuario insertado
        user_id = cursor.lastrowid
        
        print(f"✅ [DB] User created successfully with ID: {user_id}")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        # Retornar respuesta exitosa
        response = UserResponse(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True
        )
        
        print(f"🎉 [SUCCESS] Registration completed for: {user_data.email}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        raise
        
    except pymysql.Error as e:
        print(f"❌ [DB ERROR] Database error: {e}")
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    except Exception as e:
        print(f"❌ [ERROR] Unexpected error: {e}")
        print(f"📋 [TRACEBACK] {traceback.format_exc()}")
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Agregar middleware CORS simple
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

if __name__ == "__main__":
    print("🚀 Starting EDMS Simple Registration Server...")
    print("📡 Server will be available at: http://localhost:8001")
    print("📋 Health check: http://localhost:8001/health")
    print("🔗 Registration endpoint: http://localhost:8001/api/v1/auth/register")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001, 
        log_level="info",
        access_log=True
    )