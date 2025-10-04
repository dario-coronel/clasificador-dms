"""
Test mode configuration - runs without database
"""
from pydantic_settings import BaseSettings
from typing import List, Optional

class TestSettings(BaseSettings):
    # Application
    APP_NAME: str = "EDMS API (Test Mode)"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Test mode flag
    TEST_MODE: bool = True
    
    # Security
    SECRET_KEY: str = "test-secret-key-for-development-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: str = "50MB"
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx,txt,png,jpg,jpeg,gif"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        case_sensitive = True

# Create test settings instance
test_settings = TestSettings()