# 🚀 CapRover Deployment Guide

This guide will help you deploy the Reddit AI Newsletter Generator to your CapRover server.

## 📋 Prerequisites

- CapRover server running and accessible
- CapRover CLI installed (`npm install -g caprover`)
- Your CapRover server configured and logged in
- OpenRouter API key (required)
- Reddit API credentials (optional - uses demo data if not provided)

## 🎯 Deployment Methods

### **Method 1: GitHub Repository Deployment (Recommended)**

#### Step 1: Create App in CapRover Dashboard

1. **Login to CapRover Dashboard**: `https://your-caprover-domain.com`
2. **Go to Apps**: Click on "Apps" in the sidebar
3. **Create New App**: 
   - App Name: `reddit-newsletter`
   - Check "Has Persistent Data" if you want to persist logs
4. **Click "Create New App"**

#### Step 2: Configure Environment Variables

In the CapRover dashboard, go to your app and set these environment variables:

**Required Variables:**
```bash
OPENAI_API_KEY=sk-or-v1-your-openrouter-api-key-here-64-characters-long
SECRET_KEY=your-super-secure-secret-key-here-generate-random-string
```

**Optional Variables (for live Reddit data):**
```bash
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=RedditNewsletterBot/1.0
```

**Configuration Variables:**
```bash
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
FLASK_ENV=production
FLASK_DEBUG=false
```

#### Step 3: Deploy from GitHub

1. **Go to Deployment Tab** in your app
2. **Select "Deploy from Github/Bitbucket/Gitlab"**
3. **Repository Info**:
   - Repository: `https://github.com/rubenjpmartins/CrewAI-Reddit-Newsletter-Docker`
   - Branch: `main`
   - Username: Leave empty for public repo
   - Password: Leave empty for public repo
4. **Click "Deploy Now"**

#### Step 4: Configure Domain & HTTPS

1. **Go to HTTP Settings** tab
2. **Enable HTTPS**: Recommended for production
3. **Custom Domain**: Set up your custom domain if desired
4. **Force HTTPS**: Enable for security

### **Method 2: CapRover CLI Deployment**

#### Step 1: Setup CapRover CLI

```bash
# Install CapRover CLI (if not already installed)
npm install -g caprover

# Login to your CapRover server
caprover login
```

#### Step 2: Deploy from Local Directory

```bash
# Navigate to your project directory
cd /path/to/CrewAI-Reddit-Newsletter-Docker

# Deploy to CapRover
caprover deploy
```

Follow the prompts:
- **App Name**: `reddit-newsletter`
- **Captain Definition**: Use existing `captain-definition` file

#### Step 3: Set Environment Variables via CLI

```bash
# Set required environment variables
caprover api --caproverUrl https://your-caprover-domain.com --path "/user/apps/appDefinitions/reddit-newsletter" --method POST --data '{
  "envVars": [
    {"key": "OPENAI_API_KEY", "value": "sk-or-v1-your-openrouter-api-key-here"},
    {"key": "SECRET_KEY", "value": "your-super-secure-secret-key-here"},
    {"key": "REDDIT_CLIENT_ID", "value": "your_reddit_client_id"},
    {"key": "REDDIT_CLIENT_SECRET", "value": "your_reddit_client_secret"},
    {"key": "REDDIT_USER_AGENT", "value": "RedditNewsletterBot/1.0"},
    {"key": "OPENROUTER_MODEL", "value": "mistralai/mistral-7b-instruct"},
    {"key": "FLASK_ENV", "value": "production"},
    {"key": "FLASK_DEBUG", "value": "false"}
  ]
}'
```

## 🔧 Getting Your API Keys

### **OpenRouter API Key (Required)**

1. **Go to OpenRouter**: https://openrouter.ai/
2. **Sign up** for an account
3. **Go to Dashboard → Keys**
4. **Create a new API key**
5. **Copy the key** (starts with `sk-or-v1-`)

### **Reddit API Credentials (Optional)**

1. **Go to Reddit Apps**: https://www.reddit.com/prefs/apps
2. **Click "Create App"** or "Create Another App"
3. **Choose "script"** as the app type
4. **Fill in the details**:
   - Name: `Reddit Newsletter Generator`
   - Description: `AI-powered newsletter from Reddit content`
   - About URL: `https://your-app-domain.com`
   - Redirect URI: `http://localhost:8080` (not used, but required)
5. **Copy the client ID and secret**

### **Generate Secret Key**

```bash
# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 🔧 Configuration Details

### **Environment Variables Explained**

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenRouter API key | ✅ Yes | `sk-or-v1-...` |
| `SECRET_KEY` | Flask session secret | ✅ Yes | `a1b2c3d4e5f6...` |
| `REDDIT_CLIENT_ID` | Reddit API client ID | ❌ No | `abc123xyz` |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | ❌ No | `secret123` |
| `REDDIT_USER_AGENT` | Reddit API user agent | ❌ No | `RedditNewsletterBot/1.0` |
| `OPENROUTER_MODEL` | AI model to use | ❌ No | `mistralai/mistral-7b-instruct` |
| `FLASK_ENV` | Flask environment | ❌ No | `production` |
| `FLASK_DEBUG` | Debug mode | ❌ No | `false` |

## 🚀 Deployment Process

### **What Happens During Deployment**

1. **CapRover pulls** your code from GitHub
2. **Docker builds** the image using your Dockerfile
3. **Container starts** with your environment variables
4. **Health checks** verify the application is running
5. **Reverse proxy** routes traffic to your app

### **Expected Build Time**

- **First deployment**: 3-5 minutes (downloading dependencies)
- **Subsequent deployments**: 1-2 minutes (using cached layers)

## 🔍 Monitoring & Troubleshooting

### **Check Application Status**

1. **CapRover Dashboard**: Monitor app status and logs
2. **Health Check**: Visit `https://your-app-url.com/health`
3. **API Status**: Visit `https://your-app-url.com/api-status`

### **Test Your Deployment**

```bash
# Health check
curl https://your-app-url.com/health

# Generate a test newsletter
curl "https://your-app-url.com/generate-newsletter?subreddit=programming"

# Access the web interface
# Open https://your-app-url.com in your browser
```

### **View Logs**

```bash
# Via CapRover CLI
caprover logs --app reddit-newsletter

# Or in CapRover Dashboard
# Go to Apps > reddit-newsletter > App Logs
```

### **Common Issues & Solutions**

#### **Build Failures**
- **Missing captain-definition file**: Ensure file exists in root
- **Dockerfile syntax errors**: Check Dockerfile syntax
- **Dependency conflicts**: Review requirements.txt

#### **Runtime Errors**
- **Missing OPENAI_API_KEY**: Set in environment variables
- **Invalid API key**: Verify OpenRouter API key is correct
- **Port issues**: CapRover should handle this automatically

#### **Application Not Responding**
```bash
# Check if container is running
# In CapRover dashboard: Apps > reddit-newsletter > App Logs

# Verify environment variables are set
# In CapRover dashboard: Apps > reddit-newsletter > App Configs > Environment Variables
```

## 🔄 Updates & Maintenance

### **Updating the Application**

#### **Method 1: GitHub Auto-Deploy**
1. **Push changes** to your GitHub repository
2. **CapRover Dashboard**: Go to Deployment tab
3. **Click "Deploy Now"** to pull latest changes

#### **Method 2: CLI Update**
```bash
# Pull latest changes locally
git pull origin main

# Deploy updated version
caprover deploy
```

### **Scaling**

```bash
# Scale to multiple instances (in CapRover dashboard)
# Go to App Configs > Instance Count
# Increase for higher availability and better performance
```

## 🛡️ Security Considerations

### **Production Security Checklist**

- ✅ **HTTPS Enabled**: Force HTTPS in CapRover
- ✅ **Environment Variables**: Never commit secrets to Git
- ✅ **API Keys**: Use environment variables only
- ✅ **Secret Key**: Generate and store securely
- ✅ **Regular Updates**: Keep dependencies updated
- ✅ **Input Validation**: Application includes built-in validation

### **Backup Strategy**

```bash
# Backup environment variables
caprover api --path "/user/apps/appDefinitions/reddit-newsletter" --method GET

# Save the output to a secure location
```

## 📊 Performance Optimization

### **Resource Allocation**

```bash
# In CapRover Dashboard > App Configs:
# - Memory: 512MB minimum, 1GB recommended
# - CPU: 0.5 cores minimum, 1 core recommended
# - Instance Count: 1 for development, 2+ for production
```

### **Performance Tips**

- **Memory**: The AI processing requires at least 512MB RAM
- **CPU**: Newsletter generation is CPU-intensive
- **Scaling**: Use multiple instances for high traffic
- **Caching**: Application includes intelligent demo data caching

## 🎉 Success!

Once deployed, your Reddit AI Newsletter Generator will be available at:
`https://reddit-newsletter.your-caprover-domain.com`

### **Test the Deployment**

1. **Health Check**: `https://your-app-url.com/health`
2. **API Status**: `https://your-app-url.com/api-status`
3. **Web Interface**: Open `https://your-app-url.com` in browser
4. **Generate Newsletter**: Test with any subreddit name
5. **API Endpoint**: `https://your-app-url.com/generate-newsletter?subreddit=programming`

### **Available Features**

- ✅ **Any Subreddit**: Generate newsletters for any public subreddit
- ✅ **AI Analysis**: Intelligent content analysis and summarization
- ✅ **Modern UI**: Responsive web interface with real-time updates
- ✅ **API Access**: RESTful API for programmatic access
- ✅ **Demo Mode**: Works without Reddit API using intelligent demo data
- ✅ **Security**: Production-ready with comprehensive security measures

---

**🚀 Your Reddit AI Newsletter Generator is now running on CapRover!**

Need help? Check the logs in CapRover dashboard or contact support. 