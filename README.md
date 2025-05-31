# Reddit AI Newsletter Generator

An AI-powered newsletter generator that creates intelligent summaries of Reddit content using OpenRouter API and Flask web interface. **Docker-only deployment** for consistent, production-ready containerized applications.

## 🏗️ Project Structure

```
CrewAI-Reddit-Newsletter-Docker/
├── 📦 app/                       # Flask application package
│   ├── __init__.py              # App package initialization
│   ├── main.py                  # Flask routes and application logic
│   ├── core/                    # Core business logic
│   │   ├── __init__.py         # Core package exports
│   │   └── reddit_newsletter.py # Newsletter generation logic
│   ├── static/                  # Static web assets
│   │   └── css/style.css       # Main application styles
│   └── templates/              # Jinja2 HTML templates
│       ├── index.html          # Main dashboard
│       └── newsletter.html     # Newsletter interface
├── ⚙️ config/                    # Configuration management
│   ├── __init__.py             # Configuration module
│   ├── env_complete_example    # Detailed environment template
│   └── env.example             # Simple environment template
├── 📚 docs/                      # Documentation
│   └── *.md                    # Project documentation
├── 🚀 wsgi.py                   # WSGI entry point for production
├── 🛠️ setup.sh                  # Environment setup script
├── 📋 requirements.txt          # Python dependencies
├── 🐳 Dockerfile               # Container definition
├── 🔧 docker-compose.yml       # Multi-container setup
├── 🔒 .dockerignore            # Docker build exclusions
└── 🌍 .env                     # Environment variables (create from template)
```

## 💾 Installation

### Prerequisites
- **Docker** (version 20.0 or higher)
- **Docker Compose** (version 1.29 or higher)
- **Git** for cloning the repository

### System Requirements
- **Memory**: Minimum 512MB RAM
- **Storage**: 500MB available disk space
- **Network**: Internet connection for API access

### Quick Installation
```bash
# Clone the repository
git clone <repository-url>
cd CrewAI-Reddit-Newsletter-Docker

# Set up environment
./setup.sh

# Start the application
docker-compose up -d
```

### Manual Installation
```bash
# 1. Clone and navigate
git clone <repository-url>
cd CrewAI-Reddit-Newsletter-Docker

# 2. Create environment file
cp config/env.example .env

# 3. Edit .env with your API keys
nano .env  # or your preferred editor

# 4. Build and start
docker-compose up --build -d

# 5. Verify installation
curl http://localhost:5000/health
```

## 🚀 Usage

### Basic Usage
1. **Access the Web Interface**: Open http://localhost:3000 in your browser
2. **Select a Subreddit**: Enter any subreddit name (e.g., "programming", "MachineLearning", "technology")
3. **Generate Newsletter**: Click "Generate Newsletter" to create AI-powered content analysis
4. **View Results**: Read the generated newsletter with clickable links and insights

### API Endpoints
- `GET /` - Main dashboard interface
- `GET /newsletter-ui?subreddit=<name>` - Newsletter interface for specific subreddit
- `GET /generate-newsletter?subreddit=<name>` - Generate newsletter via API
- `GET /health` - Application health check
- `GET /api-status` - Configuration and API status

### Environment Configuration
The application automatically detects your environment setup:
- **With Reddit API**: Uses live Reddit data for accurate content
- **Without Reddit API**: Uses intelligent demo data for testing
- **OpenRouter API**: Required for AI-powered content analysis

### Subreddit Selection
You can generate newsletters for any public subreddit:
- **Technology**: programming, MachineLearning, technology, webdev
- **Science**: science, datascience, artificial
- **Business**: entrepreneur, startups, business
- **Custom**: Any public subreddit name

## 🚀 Quick Start (Docker Only)

### 1. Prerequisites
- Docker & Docker Compose installed
- API keys from OpenRouter (required) and Reddit (optional)

### 2. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd CrewAI-Reddit-Newsletter-Docker

# Set up environment variables (choose one method)

# Method 1: Use the setup script (recommended)
./setup.sh

# Method 2: Manual setup
cp config/env.example .env
# Then edit .env with your API keys
```

### 3. Configure API Keys

Edit the `.env` file with your credentials:

```env
# Required: OpenRouter API
OPENAI_API_KEY=sk-or-v1-your-openrouter-api-key-here-64-characters-long

# Required: Flask Security
SECRET_KEY=26041605ffc6c6a719bf99dc50627ef4ead230d59a0925872c030eee942b5b3a

# Optional: Reddit API (uses demo data if not provided)
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=RedditNewsletterBot/1.0
```

### 4. Get Your API Keys

#### OpenRouter API (Required)
1. Go to https://openrouter.ai/
2. Sign up for an account
3. Go to Dashboard → Keys
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-`)

#### Reddit API (Optional)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the details and create
5. Copy the client ID and secret

### 5. Start with Docker Compose

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Access the application**: http://localhost:5000

## 🔧 Configuration

The application uses a centralized configuration system in `config/__init__.py`:

- **Environment Variables**: Loaded from `.env` file
- **Flask Settings**: Host, port, debug mode
- **API Configuration**: OpenRouter and Reddit API settings
- **Production Settings**: Gunicorn WSGI server configuration

## 📁 Key Components

### Flask Application (`app/main.py`)
- **Routes**: Web endpoints for the application
- **API Status**: Real-time configuration checking
- **Newsletter Generation**: AI-powered content creation
- **Log Streaming**: Real-time application logs

### Core Logic (`app/core/reddit_newsletter.py`)
- **Reddit Scraping**: Content extraction from subreddits
- **AI Analysis**: OpenRouter-powered content analysis
- **Newsletter Creation**: Structured newsletter generation
- **Demo Data**: Fallback content when APIs unavailable

### WSGI Entry Point (`wsgi.py`)
- **Production Server**: Gunicorn-compatible entry point
- **Configuration**: Centralized settings management
- **Logging**: Application startup and configuration logging

## 🎨 Frontend

### Templates
- **Modern UI**: Responsive design with CSS Grid/Flexbox
- **Real-time Updates**: Live status indicators and progress bars
- **API Integration**: Dynamic content loading via JavaScript

### Static Assets
- **CSS**: Custom styling with CSS variables
- **Responsive Design**: Mobile-friendly interface
- **Progressive Enhancement**: Works without JavaScript

## 🔒 Security & Production

- **Containerized**: Isolated environment with non-root user
- **Environment Variables**: Sensitive data in `.env` file
- **WSGI Server**: Production-grade Gunicorn server
- **Health Checks**: Built-in container health monitoring
- **Secret Key**: Flask session encryption
- **Input Validation**: Secure data handling

## 🐳 Docker Deployment Options

### Development
```bash
# Quick development start
docker-compose up

# With rebuild
docker-compose up --build
```

### Production
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# Scale workers
docker-compose up -d --scale reddit-newsletter=3
```

### Container Management
```bash
# View running containers
docker-compose ps

# Check health status
docker-compose exec reddit-newsletter curl http://localhost:5000/health

# Update application
docker-compose pull && docker-compose up -d

# View real-time logs
docker-compose logs -f reddit-newsletter
```

## 📊 Monitoring & Health Checks

### Built-in Health Check
The container includes automatic health monitoring:
- **Endpoint**: `GET /health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts

### Log Management
```bash
# View application logs
docker-compose logs reddit-newsletter

# Follow logs in real-time
docker-compose logs -f

# Container logs location
docker exec -it reddit-newsletter ls /tmp/
```

## 📚 API Endpoints

- `GET /` - Main dashboard
- `GET /newsletter-ui` - Newsletter interface
- `GET /generate-newsletter` - Create new newsletter
- `GET /newsletter-status` - Check generation status
- `GET /api-status` - Configuration status
- `GET /health` - Application health check
- `GET /logs` - Real-time log streaming

## ⚙️ Environment Variables

### Required
- `OPENAI_API_KEY` - OpenRouter API key
- `SECRET_KEY` - Flask session encryption key

### Optional
- `OPENROUTER_MODEL` - AI model selection (default: mistralai/mistral-7b-instruct)
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API client secret
- `REDDIT_USER_AGENT` - Reddit API user agent
- `FLASK_ENV` - Environment mode (development/production)
- `FLASK_DEBUG` - Debug mode (true/false)

## 🔧 Development

### Local Development with Docker
```bash
# Development mode with auto-reload
docker-compose -f docker-compose.yml up

# Access container shell
docker-compose exec reddit-newsletter /bin/bash

# Run tests inside container
docker-compose exec reddit-newsletter python -m pytest
```

### Code Changes
1. **Core Logic**: Modify `app/core/`
2. **Web Routes**: Update `app/main.py`
3. **Templates**: Edit `app/templates/`
4. **Styles**: Modify `app/static/css/`
5. **Configuration**: Update `config/__init__.py`
6. **Rebuild**: `docker-compose up --build`

## 🚧 Troubleshooting

### Common Issues

1. **Container Won't Start**
   ```bash
   # Check logs
   docker-compose logs reddit-newsletter
   
   # Verify environment variables
   docker-compose config
   ```

2. **Health Check Failures**
   ```bash
   # Manual health check
   docker-compose exec reddit-newsletter curl http://localhost:5000/health
   
   # Check container status
   docker-compose ps
   ```

3. **Port Conflicts**
   ```bash
   # Use different port
   docker-compose up -d --scale reddit-newsletter=1 -p 8080:5000
   ```

4. **API Key Issues**
   ```bash
   # Verify environment variables are loaded
   docker-compose exec reddit-newsletter env | grep OPENAI_API_KEY
   ```

### Performance Optimization
- **Worker Scaling**: Adjust `--workers` in Dockerfile
- **Memory Limits**: Add memory constraints to docker-compose.yml
- **CPU Limits**: Configure CPU allocation for containers

## 📄 License

See `docs/LICENSE` for license information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker: `docker-compose up --build`
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check container logs: `docker-compose logs -f`
2. Verify health status: `docker-compose ps`
3. Test health endpoint: `curl http://localhost:5000/health`
4. Review environment configuration: `docker-compose config` 