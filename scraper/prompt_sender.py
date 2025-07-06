"""
Prompt sending functionality for ChatGPT scraper.
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from .utils import CHATGPT_RESPONSE_SELECTOR, MIN_WAIT_TIME, MAX_WAIT_TIME, TEXT_CHECK_INTERVAL

logger = logging.getLogger(__name__)


class PromptSender:
    """Handles sending prompts to ChatGPT and waiting for responses."""
    
    def __init__(self, driver):
        """Initialize prompt sender with browser driver."""
        self.driver = driver
    
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to ChatGPT and wait for response.
        
        Args:
            prompt: The prompt to send
            
        Returns:
            The response text from ChatGPT
        """
        # Wait for the input area to be available
        wait = WebDriverWait(self.driver, 10)
        input_div = wait.until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
        
        # Clear any existing content and type the prompt
        input_div.clear()
        input_div.send_keys(prompt)
        logger.info(f"Sent prompt: {prompt[:50]}...")
        
        # Press Enter to send
        input_div.send_keys('\n')
        
        # Wait for response to start appearing
        time.sleep(4)
        
        # Wait for response to complete (look for the assistant response)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CHATGPT_RESPONSE_SELECTOR)))
        
        # Wait for ChatGPT to finish typing
        logger.info("Waiting for ChatGPT to finish typing...")
        start_time = time.time()
        
        while time.time() - start_time < MAX_WAIT_TIME:
            try:
                # Retry up to 3 times for StaleElementReferenceException
                for attempt in range(3):
                    try:
                        response_elements = self.driver.find_elements(By.CSS_SELECTOR, CHATGPT_RESPONSE_SELECTOR)
                        if response_elements:
                            last_response = response_elements[-1]
                            current_text = last_response.text
                            time.sleep(TEXT_CHECK_INTERVAL)
                            new_text = last_response.text
                            if time.time() - start_time >= MIN_WAIT_TIME:
                                if current_text == new_text:
                                    logger.info("ChatGPT finished typing")
                                    break
                                else:
                                    logger.info("ChatGPT is still typing, waiting...")
                                    continue
                            else:
                                logger.info(f"Waiting minimum time... ({int(time.time() - start_time)}s/{MIN_WAIT_TIME}s)")
                                continue
                        break  # If no exception, break retry loop
                    except StaleElementReferenceException as se:
                        logger.warning(f"StaleElementReferenceException (attempt {attempt+1}/3): {se}")
                        if attempt == 2:
                            raise
                        time.sleep(1)
                else:
                    # If we exhausted retries, break outer loop
                    break
            except Exception as e:
                logger.warning(f"Error checking typing status: {e}")
                break
        
        # Wait a bit more for the full response
        time.sleep(3)
        
        # Extract the response
        from .response_handler import ResponseExtractor
        extractor = ResponseExtractor(self.driver)
        response = extractor.extract_response()
        
        # Validate response - if empty or too short, raise exception to trigger retry
        if not response or len(response.strip()) < 50:
            logger.warning(f"Received empty or too short response: '{response[:100]}...'")
            raise Exception("Empty or invalid response received from ChatGPT")
        
        return response 