"""
Brand mention analysis and extraction.
"""
import logging
from typing import Dict

from .utils import BRANDS, create_brand_patterns

logger = logging.getLogger(__name__)


class BrandAnalyzer:
    """Handles brand mention extraction and analysis."""
    
    def __init__(self):
        """Initialize brand analyzer."""
        self.brand_patterns = create_brand_patterns()
    
    def extract_brand_mentions(self, text: str) -> Dict[str, int]:
        """
        Extract brand mentions from text using regex patterns.
        
        Args:
            text: Text to analyze for brand mentions
            
        Returns:
            Dictionary with brand names and mention counts
        """
        mentions = {brand: 0 for brand in BRANDS}
        
        for brand, pattern in self.brand_patterns.items():
            matches = pattern.findall(text)
            mentions[brand] = len(matches)
            
        return mentions
    
    def log_mentions(self, mentions: Dict[str, int]):
        """
        Log brand mentions found in response.
        
        Args:
            mentions: Dictionary of brand mentions
        """
        logger.info("Brand mentions found:")
        for brand, count in mentions.items():
            if count > 0:
                logger.info(f"  - {brand}: {count}") 