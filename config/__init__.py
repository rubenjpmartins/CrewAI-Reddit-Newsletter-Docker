"""
Configuration module for Reddit AI Newsletter Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
    
    # OpenRouter/AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
    
    # Reddit API Configuration (Optional)
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    
    # Application Settings
    LOG_FILE = "/tmp/app.log"
    LOG_LEVEL = "INFO"
    
    @property
    def is_development(self):
        return self.FLASK_ENV == "development"
    
    @property
    def has_openrouter_config(self):
        return bool(self.OPENAI_API_KEY)
    
    @property
    def has_reddit_config(self):
        return bool(self.REDDIT_CLIENT_ID and self.REDDIT_CLIENT_SECRET and self.REDDIT_USER_AGENT)

# Create singleton instance
config = Config() 