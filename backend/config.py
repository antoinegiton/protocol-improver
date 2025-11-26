# config.py - Configuration and settings for Protocol Improver

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"  # Latest Claude model
    
    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 10  # Maximum file size in megabytes
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".doc"}
    UPLOAD_FOLDER: str = "../uploads"
    OUTPUT_FOLDER: str = "../outputs"
    
    # Analysis Settings
    MAX_TOKENS: int = 4000  # Maximum tokens for Claude response
    TEMPERATURE: float = 0.3  # Lower = more focused, higher = more creative
    
    # Priority Levels
    PRIORITY_HIGH: str = "HIGH"
    PRIORITY_MEDIUM: str = "MEDIUM"
    PRIORITY_LOW: str = "LOW"
    
    # Issue Categories
    ISSUE_CATEGORIES = [
        "safety",
        "clarity",
        "completeness",
        "formatting",
        "best_practices"
    ]
    
    @classmethod
    def validate(cls):
        """Validate that all required settings are present"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please add it to your .env file"
            )
        
        if not cls.ANTHROPIC_API_KEY.startswith("sk-ant-"):
            raise ValueError(
                "ANTHROPIC_API_KEY appears to be invalid. It should start with 'sk-ant-'"
            )
        
        # Create folders if they don't exist
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.OUTPUT_FOLDER, exist_ok=True)
        
        return True

# Create a settings instance
settings = Settings()

# Validate settings on import
try:
    settings.validate()
    print("✅ Configuration loaded successfully")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    raise
