"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/redaction_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"

    # OCR Settings
    TESSERACT_CMD: str = "tesseract"

    # NLP Models
    SPACY_MODEL: str = "en_core_web_sm"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
