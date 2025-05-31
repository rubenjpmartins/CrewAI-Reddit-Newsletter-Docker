#!/bin/bash
echo "🚀 Reddit AI Newsletter Generator - Environment Setup"
echo "=================================================="
echo

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists."
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Copy the example file
if [ -f "config/env.example" ]; then
    cp config/env.example .env
    echo "✅ Created .env file from template"
else
    echo "❌ Template file config/env.example not found"
    exit 1
fi

echo
echo "📝 Next steps:"
echo "1. Edit the .env file with your actual API keys:"
echo "   - Get OpenRouter API key from: https://openrouter.ai/"
echo "   - Get Reddit API credentials from: https://www.reddit.com/prefs/apps"
echo
echo "2. Start the application with Docker:"
echo "   docker-compose up -d"
echo
echo "3. Access the app at: http://localhost:5000"
echo

echo "🔧 To generate a secure SECRET_KEY, run:"
echo "python3 -c \"import secrets; print(secrets.token_hex(32))\"" 