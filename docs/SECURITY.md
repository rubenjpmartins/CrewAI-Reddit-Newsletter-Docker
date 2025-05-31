# Security Guidelines

## 🔒 Security Checklist for Public Repository

This document outlines the security measures implemented in this project and guidelines for safe deployment.

## ✅ Implemented Security Measures

### 1. **Credential Management**
- ✅ No hardcoded API keys or secrets in source code
- ✅ All sensitive data stored in environment variables
- ✅ `.env` file properly ignored in `.gitignore`
- ✅ `credentials.json` and `token.json` excluded from repository
- ✅ Base64 encoding for Google credentials in containers
- ✅ Placeholder values in documentation (not real credentials)

### 2. **Flask Application Security**
- ✅ Secret key loaded from environment variable
- ✅ Debug mode disabled by default (controlled via `FLASK_DEBUG` env var)
- ✅ OAuth state validation to prevent CSRF attacks
- ✅ Session timeout (10 minutes for OAuth flows)
- ✅ Duplicate request prevention for OAuth callbacks
- ✅ Proper error handling without exposing sensitive information

### 3. **Docker Security**
- ✅ Non-root user in Docker container
- ✅ Minimal base image (python:3.11-slim)
- ✅ `.dockerignore` excludes sensitive files
- ✅ Environment variables for configuration
- ✅ No secrets baked into Docker image

### 4. **OAuth Security**
- ✅ Proper OAuth 2.0 flow implementation
- ✅ State parameter validation
- ✅ Secure redirect URI validation
- ✅ Token refresh handling
- ✅ Session-based credential storage

### 5. **API Security**
- ✅ OpenRouter API key stored securely
- ✅ Rate limiting considerations (handled by OpenRouter)
- ✅ Proper error handling for API failures
- ✅ No API keys logged or exposed in responses

## 🚨 Security Requirements for Deployment

### Environment Variables (Required)
```bash
# OpenRouter API Configuration
OPENAI_API_KEY=sk-or-v1-your-actual-openrouter-key

# Flask Security
SECRET_KEY=your-cryptographically-secure-random-string

# Google OAuth (choose one method)
GOOGLE_CREDENTIALS_BASE64=your-base64-encoded-credentials
# OR
# Mount credentials.json file securely

# Optional Security Settings
FLASK_DEBUG=false  # NEVER set to true in production
GOOGLE_REDIRECT_URI=https://yourdomain.com/callback
```

### Production Deployment Checklist

#### Before Deployment:
- [ ] Generate a strong, random `SECRET_KEY` (minimum 32 characters)
- [ ] Verify `FLASK_DEBUG` is set to `false` or not set
- [ ] Ensure all API keys are valid and have appropriate permissions
- [ ] Configure proper redirect URIs in Google Cloud Console
- [ ] Review and limit Google OAuth scopes to minimum required

#### Google Cloud Console Setup:
- [ ] Enable Gmail API and Google Calendar API
- [ ] Create OAuth 2.0 credentials with correct redirect URIs
- [ ] Add your production domain to authorized domains
- [ ] Download credentials.json and convert to base64 for containers

#### Container Security:
- [ ] Use environment variables for all secrets
- [ ] Never include credentials in Docker image
- [ ] Use Docker secrets or secure environment injection
- [ ] Regularly update base images for security patches

## 🛡️ Security Best Practices

### 1. **API Key Management**
- Use different API keys for development and production
- Regularly rotate API keys
- Monitor API usage for unusual activity
- Set up billing alerts for unexpected usage

### 2. **Google OAuth Security**
- Use the minimum required scopes
- Regularly review OAuth consent screen
- Monitor for unauthorized access attempts
- Implement proper session management

### 3. **Container Security**
- Keep base images updated
- Scan images for vulnerabilities
- Use multi-stage builds to minimize attack surface
- Run containers with non-root users

### 4. **Network Security**
- Use HTTPS in production (handled by reverse proxy)
- Implement proper CORS policies if needed
- Consider rate limiting at the reverse proxy level
- Monitor for suspicious traffic patterns

## 🔍 Security Monitoring

### Logs to Monitor:
- Failed OAuth attempts
- API rate limit hits
- Unusual error patterns
- Session timeout events

### Alerts to Set Up:
- High API usage
- Authentication failures
- Application errors
- Container resource usage

## 📋 Incident Response

### If Credentials are Compromised:
1. **Immediately** revoke the compromised credentials
2. Generate new API keys/secrets
3. Update all deployment environments
4. Review logs for unauthorized access
5. Notify users if data may have been accessed

### If Repository is Compromised:
1. Change all API keys and secrets
2. Review commit history for exposed credentials
3. Force-push cleaned history if needed
4. Update all deployments with new credentials

## 🔗 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google OAuth 2.0 Security Best Practices](https://developers.google.com/identity/protocols/oauth2/security-best-practices)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)

## 📞 Reporting Security Issues

If you discover a security vulnerability, please:
1. **DO NOT** open a public issue
2. Email the maintainer directly
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be addressed before public disclosure

---

**Last Updated:** May 30, 2025
**Security Review:** ✅ Passed 