#!/usr/bin/env python3
"""
Brand Mentions Scraper - Entry Point

This script is the main entry point for the Brand Mentions Analysis System.
It uses undetected-chromedriver to scrape ChatGPT responses and analyze brand mentions.

Usage:
    python scraper.py --password <db_password> [--delay <seconds>]

Example:
    python scraper.py --password mypassword --delay 5
"""

from scraper.main import main

if __name__ == "__main__":
    main() 