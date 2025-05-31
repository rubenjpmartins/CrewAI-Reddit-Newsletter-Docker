# Reddit AI Newsletter Generator

A Flask web application that uses AI agents to generate engaging newsletters from the latest content on the LocalLLaMA subreddit. The application scrapes Reddit posts, analyzes them using AI agents, and creates a formatted newsletter with insights and project links.

## Features

- 🤖 **AI-Powered Analysis**: Uses CrewAI agents to research, write, and critique content
- 📰 **Reddit Integration**: Scrapes hot posts from r/LocalLLaMA subreddit
- 🎨 **Modern Web Interface**: Beautiful, responsive UI for newsletter generation
- 🔄 **Real-time Processing**: Live status updates and log streaming
- 🌐 **OpenRouter Integration**: Supports multiple AI models via OpenRouter API

## Architecture

The application uses three specialized AI agents:

1. **Explorer Agent**: Scrapes and analyzes Reddit content to identify trending AI projects
2. **Writer Agent**: Creates engaging newsletter content in markdown format
3. **Critic Agent**: Reviews and refines the content for clarity and engagement

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd reddit-newsletter-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example environment file and fill in your credentials:
```bash
cp env_complete_example .env
```

Edit `.env` with your actual values:
```env
# OpenRouter API (Required)
OPENAI_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=mistralai/mistral-7b-instruct

# Flask Configuration
SECRET_KEY=your_super_secure_secret_key_here

# Reddit API (Optional - uses demo data if not configured)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_app_name_v1.0
```

### 4. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` to access the web interface.

## Configuration

### OpenRouter API Setup
1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key from the dashboard
3. Choose your preferred AI model (see supported models below)

### Reddit API Setup (Optional)
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Copy the client ID and secret
5. Create a descriptive user agent string

### Supported AI Models
- `anthropic/claude-3.5-sonnet` (recommended)
- `openai/gpt-4o`
- `google/gemini-2.0-flash-exp`
- `meta-llama/llama-3.1-405b-instruct`
- `anthropic/claude-3-haiku` (budget-friendly)
- `mistralai/mistral-7b-instruct` (default)

## Usage

1. **Access the Web Interface**: Navigate to `http://localhost:5000`
2. **Check System Status**: The interface will verify your API configuration
3. **Generate Newsletter**: Click "Generate Newsletter" to start the AI agents
4. **Monitor Progress**: Watch real-time logs and status updates
5. **View Results**: The generated newsletter will appear with formatted content and links

## API Endpoints

- `GET /` - Main landing page
- `GET /newsletter-ui` - Newsletter generation interface
- `POST /generate-newsletter` - Start newsletter generation
- `GET /newsletter-status` - Check generation status
- `GET /api-status` - Check API configuration
- `GET /logs` - Stream real-time logs
- `GET /health` - Health check endpoint

## Project Structure

```
├── app.py                    # Main Flask application
├── reddit_newsletter.py     # AI agents and crew configuration
├── templates/
│   ├── index.html           # Landing page
│   └── newsletter.html      # Newsletter generation interface
├── requirements.txt         # Python dependencies
├── env_complete_example     # Environment variables template
└── README.md               # This file
```

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=true
python app.py
```

### Docker Deployment
```bash
docker build -t reddit-newsletter .
docker run -p 5000:5000 --env-file .env reddit-newsletter
```

## Troubleshooting

### Common Issues

1. **OpenRouter API Errors**: Verify your API key and model name
2. **Reddit Access Issues**: Check your Reddit API credentials
3. **Generation Timeouts**: Try a faster AI model or check your internet connection

### Logs
Real-time logs are available through the web interface or in `/tmp/app.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the logs for error details
- Open an issue on GitHub
