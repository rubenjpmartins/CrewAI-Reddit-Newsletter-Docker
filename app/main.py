from flask import Flask, jsonify, render_template, Response, request
import os
import time
import logging
import sys
import json
from datetime import datetime
from app.core.reddit_newsletter import crew
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(config.LOG_FILE)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Global variable to store the latest newsletter
latest_newsletter = None
newsletter_status = "ready"  # ready, processing, completed, error

@app.route('/')
def index():
    logger.info("Index page accessed")
    return render_template("index.html", predefined_subreddits=config.predefined_subreddits)

@app.route('/generate-newsletter')
def generate_newsletter():
    global latest_newsletter, newsletter_status
    
    # Get subreddit from query parameter, default to LocalLLaMA
    subreddit_name = request.args.get('subreddit', 'LocalLLaMA')
    
    # Basic validation for subreddit name
    if not subreddit_name or len(subreddit_name.strip()) == 0:
        subreddit_name = 'LocalLLaMA'
    
    # Clean the subreddit name (remove r/ prefix if present)
    subreddit_name = subreddit_name.strip()
    if subreddit_name.startswith('r/'):
        subreddit_name = subreddit_name[2:]
    
    logger.info(f"Starting Reddit newsletter generation for r/{subreddit_name}...")
    newsletter_status = "processing"
    
    try:
        logger.info("Starting CrewAI processing...")
        start_time = time.time()
        
        result = crew.kickoff(subreddit_name)
        
        processing_time = time.time() - start_time
        logger.info(f"CrewAI processing completed in {processing_time:.2f} seconds")
        
        latest_newsletter = {
            "content": str(result),
            "generated_at": datetime.now().isoformat(),
            "processing_time": f"{processing_time:.2f}s",
            "subreddit": subreddit_name
        }
        
        newsletter_status = "completed"
        
        return jsonify({
            "success": True,
            "newsletter": latest_newsletter,
            "processing_time": f"{processing_time:.2f}s",
            "subreddit": subreddit_name
        })
        
    except Exception as e:
        logger.error(f"Error during newsletter generation for r/{subreddit_name}: {str(e)}", exc_info=True)
        newsletter_status = "error"
        return jsonify({
            "success": False,
            "error": f"Failed to generate newsletter for r/{subreddit_name}: {str(e)}",
            "subreddit": subreddit_name
        }), 500

@app.route('/newsletter-status')
def newsletter_status_endpoint():
    return jsonify({
        "status": newsletter_status,
        "newsletter": latest_newsletter
    })

@app.route('/newsletter-ui')
def newsletter_ui():
    logger.info("Newsletter UI accessed")
    return render_template("newsletter.html")

@app.route('/logs')
def logs():
    """Stream real-time logs to the web interface"""
    def generate_logs():
        try:
            with open(config.LOG_FILE, 'r') as f:
                # Get existing logs
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        yield f"data: {line}\n\n"
                    else:
                        time.sleep(0.1)
        except FileNotFoundError:
            yield "data: Log file not found\n\n"
    
    return Response(generate_logs(), mimetype='text/event-stream')

@app.route('/api-status')
def api_status():
    """Check API configuration status"""
    status = {
        "openrouter_configured": config.has_openrouter_config,
        "model_configured": bool(config.OPENROUTER_MODEL),
        "reddit_configured": False  # Will be true when Reddit credentials are properly set
    }
    
    try:
        # Test Reddit configuration by checking if we have proper credentials
        if config.has_reddit_config:
            import praw
            reddit = praw.Reddit(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET, 
                user_agent=config.REDDIT_USER_AGENT,
            )
            # Try to access a subreddit to test credentials
            subreddit = reddit.subreddit("test")
            subreddit.display_name  # This will trigger an API call
            status["reddit_configured"] = True
        else:
            logger.info("Reddit credentials not configured in environment variables - using demo data")
            status["reddit_configured"] = True  # Demo data still works
    except Exception as e:
        logger.warning(f"Reddit configuration test failed, will use demo data: {e}")
        status["reddit_configured"] = True  # Demo data fallback
    
    return jsonify(status)

@app.route('/health')
def health():
    """Basic health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "reddit-newsletter-app"
    })