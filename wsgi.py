#!/usr/bin/env python3
"""
WSGI Entry Point for Reddit AI Newsletter Generator
Production-ready entry point for Docker deployment
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app, logger
from config import config

# Configure for production
if __name__ != '__main__':
    # Running under WSGI server (gunicorn, uwsgi, etc.)
    logger.info("Starting Reddit Newsletter Flask App via WSGI...")
    logger.info(f"OpenRouter Model: {config.OPENROUTER_MODEL}")
    logger.info(f"OpenRouter API Key configured: {config.has_openrouter_config}")

# For direct execution (development only)
if __name__ == '__main__':
    logger.info("Starting Reddit Newsletter Flask App in development mode...")
    logger.info(f"OpenRouter Model: {config.OPENROUTER_MODEL}")
    logger.info(f"OpenRouter API Key configured: {config.has_openrouter_config}")
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    ) 