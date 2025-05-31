#!/usr/bin/env python3
"""
Reddit AI Newsletter Generator - Main Entry Point
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from app.main import app, logger
    from config import config
    
    logger.info("Starting Reddit Newsletter Flask App...")
    logger.info(f"OpenRouter Model: {config.OPENROUTER_MODEL}")
    logger.info(f"OpenRouter API Key configured: {config.has_openrouter_config}")
    
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG) 