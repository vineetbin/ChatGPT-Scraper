#!/bin/bash

# Brand Mentions Analysis System - Setup Script

echo "🚀 Setting up Brand Mentions Analysis System..."

# Check if Python 3.9+ is installed
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.9 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# macOS/Homebrew: Check if PostgreSQL is running
if [[ "$(uname)" == "Darwin" ]]; then
    if ! brew services list | grep -q 'postgresql.*started'; then
        echo "⚠️  PostgreSQL does not appear to be running."
        echo "   Start it with: brew services start postgresql@14"
        echo "   Or check status with: brew services list"
        echo "   If you continue without PostgreSQL running, database setup will fail."
    else
        echo "✅ PostgreSQL service is running."
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scraper.py
chmod +x api_server.py
chmod +x scripts/database_setup.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Initialize the database: python scripts/database_setup.py --password your_password"
echo "2. Run Stage 1 (scraping): python scraper.py --password your_password"
echo "3. Run Stage 2 (API): python api_server.py --password your_password"
echo ""
echo "📖 For more information, see README.md" 