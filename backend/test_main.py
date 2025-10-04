"""
Test version of FastAPI app that runs without database
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.test_config import test_settings

# Create FastAPI application for testing
app = FastAPI(
    title=test_settings.APP_NAME,
    version=test_settings.APP_VERSION,
    description="Electronic Document Management System API - Test Mode (No Database Required)",
    openapi_url=f"{test_settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if test_settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in test_settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"Welcome to {test_settings.APP_NAME}",
        "version": test_settings.APP_VERSION,
        "status": "running",
        "mode": "test",
        "note": "This is test mode - no database required"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "mode": "test",
        "database": "not_required"
    }

# Add some example endpoints for testing
@app.get("/api/v1/test/endpoints")
async def list_endpoints():
    """List all available endpoints"""
    return {
        "available_endpoints": [
            "GET / - Root endpoint",
            "GET /health - Health check",
            "GET /docs - Swagger documentation",
            "GET /redoc - ReDoc documentation",
            "GET /api/v1/test/endpoints - This endpoint",
            "POST /api/v1/test/echo - Echo test endpoint"
        ],
        "note": "To enable full functionality, configure MySQL database"
    }

@app.post("/api/v1/test/echo")
async def echo_test(data: dict):
    """Echo endpoint for testing"""
    return {
        "message": "Echo successful",
        "received_data": data,
        "status": "test_mode"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 EDMS API - Test Mode")
    print("="*50)
    print("📋 Mode: Test (No database required)")
    print("🌐 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("="*50 + "\n")
    
    uvicorn.run(
        "test_main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )