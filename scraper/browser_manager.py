"""
Browser management for ChatGPT scraper.
"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import undetected_chromedriver as uc
from .utils import CHATGPT_URL, BROWSER_OPTIONS

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser setup and navigation for ChatGPT scraping."""
    
    def __init__(self):
        """Initialize browser manager."""
        self.driver = None
    
    def launch_browser(self):
        """Launch undetected-chromedriver browser."""
        logger.info("Launching undetected-chromedriver...")
        options = uc.ChromeOptions()
        
        # Add basic options for undetection
        for option in BROWSER_OPTIONS:
            options.add_argument(option)
        
        try:
            self.driver = uc.Chrome(options=options)
            logger.info("Browser launched successfully")
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            raise
    
    def navigate_to_chatgpt(self):
        """Navigate to ChatGPT and wait for interface to be ready."""
        logger.info("Navigating to ChatGPT...")
        self.driver.get(CHATGPT_URL)
        logger.info("Navigation completed")
        
        # Wait for page to load
        time.sleep(3)
        
        # Check if we need to handle login
        current_url = self.driver.current_url
        logger.info(f"Current URL: {current_url}")
        if "login" in current_url.lower():
            logger.warning("ChatGPT login required. Please log in manually and press Enter to continue...")
            input("Press Enter after logging in...")
        
        # Wait for chat interface to be ready
        logger.info("Waiting for chat interface...")
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
        logger.info("ChatGPT interface is ready")
    
    def handle_stay_logged_out_popup(self):
        """
        Check for and handle the "Stay logged out" popup if it appears.
        Returns True if popup was found and handled, False otherwise.
        """
        try:
            stay_logged_out_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Stay logged out')]")
            if stay_logged_out_link.is_displayed():
                logger.info("Detected 'Stay logged out' popup, clicking to dismiss...")
                stay_logged_out_link.click()
                time.sleep(2)  # Wait for popup to disappear
                return True
        except NoSuchElementException:
            # No popup found
            pass
        return False
    
    def close_browser(self):
        """Close the browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}") 