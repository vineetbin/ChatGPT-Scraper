"""
Utility functions and configuration for the scraper.
"""
import json
import logging
import re
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

# Target brands to track
BRANDS = ['nike', 'adidas', 'hoka', 'new balance', 'jordan']

# ChatGPT selectors
CHATGPT_INPUT_SELECTOR = 'textarea[data-id="root"]'
CHATGPT_RESPONSE_SELECTOR = '[data-message-author-role="assistant"]'
CHATGPT_URL = "https://chat.openai.com/"

# Timing configuration
MIN_WAIT_TIME = 30  # Minimum seconds to wait for response
MAX_WAIT_TIME = 60  # Maximum seconds to wait for response
TEXT_CHECK_INTERVAL = 2  # Seconds between text change checks

# Browser options for undetected-chromedriver
BROWSER_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage'
]


def create_brand_patterns() -> Dict[str, re.Pattern]:
    """Create regex patterns for brand detection."""
    patterns = {}
    for brand in BRANDS:
        # Handle multi-word brands like "new balance"
        if ' ' in brand:
            # For multi-word brands, match the whole phrase
            pattern = re.compile(rf'\b{re.escape(brand)}\b', re.IGNORECASE)
        else:
            # For single-word brands, match word boundaries
            pattern = re.compile(rf'\b{re.escape(brand)}\b', re.IGNORECASE)
        patterns[brand] = pattern
    return patterns


def load_prompts() -> List[str]:
    """
    Load prompts from JSON file.
    
    Returns:
        List of prompts
    """
    prompts_file = Path("data/sample_prompts.json")
    
    if not prompts_file.exists():
        logger.error(f"Prompts file not found: {prompts_file}")
        return []
    
    try:
        with open(prompts_file, 'r') as f:
            prompts = json.load(f)
        logger.info(f"Loaded {len(prompts)} prompts from {prompts_file}")
        return prompts
    except Exception as e:
        logger.error(f"Error loading prompts: {e}")
        return []


def parse_arguments():
    """Parse command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Brand Mentions Scraper')
    parser.add_argument('--db-password', type=str, required=True, help='Database password')
    parser.add_argument('--delay', type=int, default=3, help='Delay between requests in seconds')
    return parser.parse_args() 