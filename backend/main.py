"""
FastAPI EDMS Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings

try:
    from app.core.database import engine
    from app.models import Base
    from app.api.api_v1.api import api_router
    
    # Test database connection before creating tables
    with engine.connect() as conn:
        print("✅ Database connection successful")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
    
    DATABASE_READY = True
    
except Exception as e:
    print(f"⚠️  Database connection failed: {e}")
    print("🔧 API will start without database endpoints")
    DATABASE_READY = False
    api_router = None

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Electronic Document Management System API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router only if database is ready
if DATABASE_READY and api_router:
    app.include_router(api_router, prefix=settings.API_V1_STR)
    print("✅ API endpoints loaded")
else:
    print("⚠️  API endpoints not loaded - database not available")

# Mount static files for uploaded documents
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    db_status = "connected" if DATABASE_READY else "disconnected"
    return {
        "status": "healthy",
        "database": db_status,
        "api_endpoints": DATABASE_READY
    }

@app.get("/db-test")
async def database_test():
    """Test database connection"""
    if not DATABASE_READY:
        return {
            "status": "error",
            "message": "Database not available",
            "suggestion": "Check MySQL container: docker ps"
        }
    
    try:
        from app.core.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 'Database OK' as status")
            row = result.fetchone()
            return {
                "status": "success",
                "message": row[0],
                "database_url": settings.DATABASE_URL.replace(settings.DB_PASSWORD, "***")
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG,
        log_level="info"
    )