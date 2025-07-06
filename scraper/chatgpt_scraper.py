"""
ChatGPT scraper implementation using undetected-chromedriver.
"""
import time
import logging
from typing import List

from app.database import create_engine_with_password
from sqlalchemy.orm import sessionmaker
from .browser_manager import BrowserManager
from .response_handler import ResponseHandler
from .data_processor import DataProcessor

logger = logging.getLogger(__name__)


class ChatGPTScraper:
    """
    Undetected-chromedriver based scraper for ChatGPT interface.
    """
    
    def __init__(self, password: str, delay=3):
        """Initialize the scraper."""
        self.password = password
        self.db = self._create_db_session()
        self.delay = delay
        
        # Initialize components
        self.browser_manager = BrowserManager()
        self.response_handler = None
        self.data_processor = DataProcessor(self.db)
        
    def _create_db_session(self):
        """Create database session with password."""
        engine = create_engine_with_password(self.password)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    
    def process_prompts(self, prompts: List[str]):
        """
        Process a list of prompts and extract brand mentions.
        
        Args:
            prompts: List of prompts to process
        """
        logger.info(f"Starting to process {len(prompts)} prompts...")
        
        try:
            # Setup browser and navigation
            self.browser_manager.launch_browser()
            self.browser_manager.navigate_to_chatgpt()
            
            # Initialize response handler with driver
            self.response_handler = ResponseHandler(self.browser_manager.driver)
            
            # Process each prompt
            for i, prompt in enumerate(prompts, 1):
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        logger.info(f"Processing prompt {i}/{len(prompts)} (attempt {retry_count + 1}): {prompt}")
                        
                        # Send prompt to ChatGPT (with automatic popup handling)
                        response = self.response_handler.retry_with_popup_handling(
                            self.response_handler.send_prompt,
                            self.browser_manager.handle_stay_logged_out_popup,
                            prompt
                        )
                        
                        # Process the response
                        self.data_processor.process_prompt_response(prompt, response)
                        
                        # Success - break out of retry loop
                        break
                        
                    except Exception as e:
                        retry_count += 1
                        logger.error(f"Error processing prompt {i} (attempt {retry_count}): {e}")
                        
                        if retry_count >= max_retries:
                            logger.error(f"Failed to process prompt {i} after {max_retries} attempts, skipping...")
                            break
                        else:
                            logger.info(f"Retrying prompt {i} in {self.delay * 2} seconds...")
                            time.sleep(self.delay * 2)  # Longer delay before retry
                
                # Add delay between requests to be respectful
                time.sleep(self.delay)
                    
        except Exception as e:
            logger.error(f"Error in process_prompts: {e}")
            raise
        finally:
            self.browser_manager.close_browser()
        
        logger.info("Completed processing all prompts!")
    
    def close(self):
        """Close database connection."""
        self.db.close() 