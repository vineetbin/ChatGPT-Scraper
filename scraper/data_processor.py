"""
Data processing for brand mentions analysis.
"""
import logging
from typing import Dict
from sqlalchemy.orm import Session

from app.models import Prompt, BrandMention
from .brand_analyzer import BrandAnalyzer

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Handles database operations for brand mentions."""
    
    def __init__(self, db_session: Session):
        """Initialize database manager with session."""
        self.db = db_session
    
    def save_prompt_response(self, prompt_text: str, response_text: str, mentions: Dict[str, int]):
        """
        Save prompt, response, and brand mentions to database.
        
        Args:
            prompt_text: The original prompt
            response_text: The ChatGPT response
            mentions: Dictionary of brand mentions
        """
        try:
            # Save prompt and response
            prompt_record = Prompt(
                prompt_text=prompt_text,
                response_text=response_text
            )
            self.db.add(prompt_record)
            self.db.flush()  # Get the ID
            
            # Save brand mentions
            for brand, count in mentions.items():
                if count > 0:
                    mention_record = BrandMention(
                        prompt_id=prompt_record.id,
                        brand_name=brand,
                        mention_count=count
                    )
                    self.db.add(mention_record)
            
            self.db.commit()
            logger.info(f"Saved data for prompt: {prompt_text[:50]}...")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving to database: {e}")
            raise


class DataProcessor:
    """Handles brand mention extraction and database operations."""
    
    def __init__(self, db_session: Session):
        """Initialize data processor with database session."""
        self.brand_analyzer = BrandAnalyzer()
        self.db_manager = DatabaseManager(db_session)
    
    def process_prompt_response(self, prompt: str, response: str):
        """
        Process a single prompt-response pair.
        
        Args:
            prompt: The original prompt
            response: The ChatGPT response
        """
        # Extract brand mentions
        mentions = self.brand_analyzer.extract_brand_mentions(response)
        
        # Log results
        self.brand_analyzer.log_mentions(mentions)
        
        # Save to database
        self.db_manager.save_prompt_response(prompt, response, mentions) 