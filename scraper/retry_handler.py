"""
Retry handling with popup management for ChatGPT scraper.
"""
import time
import logging

logger = logging.getLogger(__name__)


class RetryHandler:
    """Handles retry logic with popup handling."""
    
    @staticmethod
    def retry_with_popup_handling(operation, popup_handler, *args, **kwargs):
        """
        Execute an operation and retry once if it fails due to popup.
        
        Args:
            operation: Function to execute
            popup_handler: Function to handle popups
            *args, **kwargs: Arguments for the operation
            
        Returns:
            Result of the operation
        """
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            
            # Try to handle popup and retry once
            if popup_handler():
                logger.info("Handled popup, retrying operation...")
                time.sleep(1)  # Brief pause after popup handling
                return operation(*args, **kwargs)
            
            # If no popup or retry also failed, re-raise the exception
            raise 