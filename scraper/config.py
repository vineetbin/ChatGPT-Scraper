"""
Scraper configuration and constants.
"""
import re
from typing import Dict

# Target brands to track
BRANDS = ['nike', 'adidas', 'hoka', 'new_balance', 'jordan']

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
        pattern = re.compile(rf'\b{re.escape(brand)}\b', re.IGNORECASE)
        patterns[brand] = pattern
    return patterns 