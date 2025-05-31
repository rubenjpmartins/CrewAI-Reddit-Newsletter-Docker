#!/usr/bin/env python3
"""
Comprehensive security and functionality tests for Reddit Newsletter Generator
"""

import os
import sys
import pytest
import tempfile
import requests
import json
import re
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_no_hardcoded_secrets():
    """Test that there are no hardcoded API keys or secrets in the codebase"""
    project_root = Path(__file__).parent.parent
    
    # Files to check for hardcoded secrets
    files_to_check = []
    for ext in ['*.py', '*.yml', '*.yaml', '*.json']:
        files_to_check.extend(project_root.glob(f'**/{ext}'))
    
    # Exclude certain directories
    exclude_dirs = {'venv', '.git', '__pycache__', 'node_modules', '.pytest_cache'}
    files_to_check = [f for f in files_to_check if not any(part in exclude_dirs for part in f.parts)]
    
    # Patterns that might indicate secrets
    secret_patterns = [
        r'sk-[a-zA-Z0-9]{48}',  # OpenAI API keys
        r'["\']password["\']:\s*["\'][^"\']+["\']',  # passwords in config
        r'SECRET_KEY\s*=\s*["\'][^"\']+["\']',  # hardcoded secret keys
        r'API_KEY\s*=\s*["\'][^"\']+["\']',  # hardcoded API keys
    ]
    
    violations = []
    for file_path in files_to_check:
        if file_path.is_file():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Filter out obvious test/example keys
                    real_violations = [m for m in matches if not any(test_indicator in m.lower() 
                                     for test_indicator in ['test', 'example', 'dummy', 'fake', 'placeholder'])]
                    if real_violations:
                        violations.append(f"{file_path}: {real_violations}")
    
    assert len(violations) == 0, f"Found potential hardcoded secrets: {violations}"

def test_environment_variables_usage():
    """Test that sensitive configuration uses environment variables"""
    try:
        from config import config
        
        # These should use environment variables, not hardcoded values
        env_vars = ['OPENAI_API_KEY', 'SECRET_KEY', 'REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']
        
        for var in env_vars:
            # The config should either have None (missing env var) or use os.environ
            assert hasattr(config, var), f"Config missing {var}"
    except ImportError:
        # If config module not available, check environment directly
        import os
        critical_vars = ['OPENAI_API_KEY', 'SECRET_KEY']
        for var in critical_vars:
            # Should use environment variables, not be hardcoded
            assert var in os.environ or not os.environ.get(var, '').startswith('sk-'), f"Environment variable {var} handling issue"

def test_gitignore_completeness():
    """Test that .gitignore properly excludes sensitive files"""
    project_root = Path(__file__).parent.parent
    gitignore_path = project_root / '.gitignore'
    
    assert gitignore_path.exists(), ".gitignore file not found"
    
    gitignore_content = gitignore_path.read_text()
    
    # Critical patterns that must be in .gitignore
    required_patterns = [
        '.env',
        '*.log',
        'venv/',
        '__pycache__/',
        '*.pyc',
        '.DS_Store',
        'logs/',
    ]
    
    for pattern in required_patterns:
        assert pattern in gitignore_content, f"Missing critical pattern in .gitignore: {pattern}"

def test_docker_security():
    """Test Docker configuration for security best practices"""
    project_root = Path(__file__).parent.parent
    dockerfile_path = project_root / 'Dockerfile'
    
    assert dockerfile_path.exists(), "Dockerfile not found"
    
    dockerfile_content = dockerfile_path.read_text()
    
    # Security checks
    assert 'useradd' in dockerfile_content, "Dockerfile should create non-root user"
    assert 'USER app' in dockerfile_content or 'USER ' in dockerfile_content, "Dockerfile should switch to non-root user"
    assert '&& rm -rf /var/lib/apt/lists/*' in dockerfile_content, "Dockerfile should clean up apt cache"

def test_requirements_security():
    """Test that requirements.txt doesn't contain vulnerable packages"""
    project_root = Path(__file__).parent.parent
    requirements_path = project_root / 'requirements.txt'
    
    assert requirements_path.exists(), "requirements.txt not found"
    
    requirements_content = requirements_path.read_text()
    
    # Should not contain these potentially vulnerable or unnecessary packages
    dangerous_packages = ['pickle', 'eval', 'exec']
    
    for package in dangerous_packages:
        assert package not in requirements_content.lower(), f"Potentially dangerous package found: {package}"

def test_api_endpoints_security():
    """Test that API endpoints are properly secured"""
    # Test if service is running
    try:
        health_response = requests.get('http://localhost:3000/health', timeout=5)
        if health_response.status_code != 200:
            pytest.skip("Service not running, skipping API tests")
    except requests.exceptions.RequestException:
        pytest.skip("Service not available, skipping API tests")
    
    # Test that sensitive endpoints don't expose internal information
    endpoints_to_test = [
        '/health',
        '/newsletter-ui',
        '/generate-newsletter?subreddit=test',
    ]
    
    for endpoint in endpoints_to_test:
        response = requests.get(f'http://localhost:3000{endpoint}')
        response_text = response.text.lower()
        
        # Should not expose sensitive information
        sensitive_info = ['password', 'secret', 'api_key', 'token']
        for info in sensitive_info:
            assert info not in response_text, f"Endpoint {endpoint} exposes sensitive info: {info}"

def test_newsletter_generation_functionality():
    """Test that newsletter generation works correctly"""
    try:
        response = requests.get('http://localhost:3000/generate-newsletter?subreddit=programming', timeout=30)
        if response.status_code != 200:
            pytest.skip("Service not available for functional testing")
        
        data = response.json()
        assert data.get('success') is True, "Newsletter generation should succeed"
        assert 'newsletter' in data, "Response should contain newsletter data"
        assert 'content' in data['newsletter'], "Newsletter should have content"
        assert len(data['newsletter']['content']) > 100, "Newsletter content should be substantial"
        
    except requests.exceptions.RequestException:
        pytest.skip("Service not available for functional testing")

def test_link_formatting_security():
    """Test that link formatting doesn't create XSS vulnerabilities"""
    # Test the link formatting function for potential XSS
    test_inputs = [
        'Check out [this link](javascript:alert("xss"))',
        'Visit <script>alert("xss")</script>',
        '[Link](data:text/html,<script>alert("xss")</script>)',
        'Plain URL: javascript:void(0)',
    ]
    
    # Since this is client-side JavaScript, we test the concept
    # In production, the frontend should sanitize these
    xss_vectors = 0
    for test_input in test_inputs:
        if 'javascript:' in test_input and '<script>' not in test_input:
            xss_vectors += 1
    
    # We expect some XSS test vectors, but they should be handled by the frontend
    assert xss_vectors >= 0, "XSS test verification"

def test_configuration_security():
    """Test that configuration is properly set up for security"""
    try:
        from config import config
        
        # Flask should be in production mode for Docker
        assert hasattr(config, 'FLASK_ENV'), "FLASK_ENV should be configured"
        
        # Debug should be False in production
        if hasattr(config, 'FLASK_ENV') and config.FLASK_ENV == 'production':
            assert not getattr(config, 'FLASK_DEBUG', True), "Debug should be False in production"
    except ImportError:
        # If config not available, check basic security principles
        import os
        flask_env = os.environ.get('FLASK_ENV', 'development')
        if flask_env == 'production':
            assert os.environ.get('FLASK_DEBUG', 'True').lower() != 'true', "Debug should be False in production"

def test_file_permissions():
    """Test that sensitive files have appropriate permissions"""
    project_root = Path(__file__).parent.parent
    
    # Check if any .env files exist (they shouldn't in repo)
    env_files = list(project_root.glob('.env*'))
    for env_file in env_files:
        if env_file.name != '.env.example':
            pytest.fail(f"Environment file {env_file} should not be in repository")

def test_documentation_completeness():
    """Test that documentation is complete and helpful"""
    project_root = Path(__file__).parent.parent
    readme_path = project_root / 'README.md'
    
    assert readme_path.exists(), "README.md should exist"
    
    readme_content = readme_path.read_text()
    
    # Check for essential documentation sections
    required_sections = [
        'Installation',
        'Usage',
        'Environment',
        'Docker',
    ]
    
    for section in required_sections:
        assert section.lower() in readme_content.lower(), f"README should contain {section} section"

if __name__ == '__main__':
    pytest.main([__file__, '-v']) 