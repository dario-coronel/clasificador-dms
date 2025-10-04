"""
Application configuration settings using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "EDMS API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://edms_user:edms_password123@localhost:3307/edms_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "edms_user"
    DB_PASSWORD: str = "edms_password123"
    DB_NAME: str = "edms_db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: str = "50MB"
    ALLOWED_FILE_TYPES: str = "pdf,doc,docx,txt,png,jpg,jpeg,gif"
    
    # OCR
    TESSERACT_PATH: str = "tesseract"
    OCR_LANGUAGES: str = "eng,spa"
    
    # Email (Optional)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()