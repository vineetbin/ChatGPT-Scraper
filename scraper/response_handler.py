"""
Response handling for ChatGPT scraper.
"""
import logging
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from .utils import CHATGPT_RESPONSE_SELECTOR
from .prompt_sender import PromptSender
from .retry_handler import RetryHandler

logger = logging.getLogger(__name__)


class ResponseExtractor:
    """Handles extracting responses from ChatGPT interface."""
    
    def __init__(self, driver):
        """Initialize response extractor with browser driver."""
        self.driver = driver
    
    def extract_response(self) -> str:
        """
        Extract response text from ChatGPT interface.
        
        Returns:
            The response text
        """
        for attempt in range(3):
            try:
                response_elements = self.driver.find_elements(By.CSS_SELECTOR, CHATGPT_RESPONSE_SELECTOR)
                if response_elements:
                    # Get the last (most recent) response
                    last_response = response_elements[-1]
                    response_text = last_response.text
                    if response_text and len(response_text.strip()) > 50:
                        logger.info(f"Received response: {len(response_text)} characters")
                        return response_text.strip()
                    else:
                        logger.warning(f"Response too short or empty: '{response_text[:100]}...'")
                break  # If no exception, break retry loop
            except StaleElementReferenceException as se:
                logger.warning(f"StaleElementReferenceException in extract_response (attempt {attempt+1}/3): {se}")
                if attempt == 2:
                    raise
                import time
                time.sleep(1)
        # Fallback: try to get any text content
        logger.warning("Using fallback response extraction")
        page_source = self.driver.page_source
        # Simple fallback - look for any large text blocks
        text_blocks = re.findall(r'<[^>]*>([^<]{100,})</[^>]*>', page_source)
        if text_blocks:
            fallback_text = text_blocks[-1][:1000]  # Return last large text block
            if len(fallback_text.strip()) > 50:
                return fallback_text
        # If we still don't have a valid response, raise an exception
        raise Exception("No valid response could be extracted from ChatGPT interface")


class ResponseHandler:
    """Handles ChatGPT interaction and response extraction."""
    
    def __init__(self, driver):
        """Initialize response handler with browser driver."""
        self.prompt_sender = PromptSender(driver)
        self.response_extractor = ResponseExtractor(driver)
    
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to ChatGPT and wait for response.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            The response text from ChatGPT
        """
        return self.prompt_sender.send_prompt(prompt)
    
    def retry_with_popup_handling(self, operation, popup_handler, *args, **kwargs):
        """
        Execute an operation and retry once if it fails due to popup.
        
        Args:
            operation: Function to execute
            popup_handler: Function to handle popups
            *args, **kwargs: Arguments for the operation
            
        Returns:
            Result of the operation
        """
        return RetryHandler.retry_with_popup_handling(operation, popup_handler, *args, **kwargs) 