"""
Configuration file for the Brand Mentions Analysis System.
"""
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_default_db_user():
    """Get default database user based on system."""
    # Check if DB_USER is explicitly set in environment
    if os.environ.get("DB_USER"):
        return os.environ.get("DB_USER")
    
    # On macOS, try to get the current user (Homebrew PostgreSQL default)
    if os.name == 'posix' and os.uname().sysname == 'Darwin':
        try:
            # Get current username
            username = subprocess.check_output(['whoami'], text=True).strip()
            return username
        except:
            pass
    
    # Fallback to postgres (Linux/Windows default)
    return "postgres"

# Database Configuration
DB_USER = get_default_db_user()
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "brand_mentions")

# API Configuration
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", "8000"))
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# Scraping Configuration
SCRAPING_DELAY = int(os.environ.get("SCRAPING_DELAY", "3"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
USER_AGENT = os.environ.get("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE = os.environ.get("LOG_FILE", "app.log")

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "brand-mentions-api-secret-key-change-in-production")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") 