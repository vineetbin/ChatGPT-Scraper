"""
Main entry point for the Brand Mentions Scraper.
"""
import logging
import sys
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from .chatgpt_scraper import ChatGPTScraper
from .utils import load_prompts, parse_arguments


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scraper.log')
        ]
    )


def main():
    """Main function to run the scraper."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Load prompts
        prompts = load_prompts()
        if not prompts:
            logger.error("No prompts loaded. Exiting.")
            sys.exit(1)
        
        # Initialize scraper
        scraper = ChatGPTScraper(
            password=args.db_password,
            delay=args.delay
        )
        
        try:
            # Process prompts
            scraper.process_prompts(prompts)
            logger.info("Scraping completed successfully!")
            
        finally:
            # Clean up
            scraper.close()
            
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 