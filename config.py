"""
Configuration file for the Patient Education Material Generator
Contains all configuration settings, API keys, and constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Main configuration class containing all app settings
    """
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Gemini API Configuration
    GEMINI_API_KEY = "AIzaSyDUId0BD0j_wIF0uhe3DQDRIkkSI0jsTnM"  # Your API key
    GEMINI_MODEL = "gemini-2.0-flash"
    
    # Database Configuration
    DATABASE_PATH = 'data/patient_education.db'
    
    # RAG Configuration
    VECTOR_DB_PATH = 'data/vector_store'
    CHUNK_SIZE = 500  # Size of text chunks for embedding
    CHUNK_OVERLAP = 50  # Overlap between chunks
    
    # Medical Knowledge Base
    KNOWLEDGE_BASE_PATH = 'data/medical_knowledge'
    
    # Education Material Types
    EDUCATION_TYPES = [
        'post_operative',      # Post-operative care instructions
        'medication_guide',    # Medication guides and instructions
        'diet_plan'           # Diet plans and nutritional guidance
    ]
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'

class DevelopmentConfig(Config):
    """
    Development-specific configuration
    """
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """
    Production-specific configuration
    """
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
