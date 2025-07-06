#!/usr/bin/env python3
"""
Database initialization script.
Sets up database schema and initial data.
"""
import logging
import argparse
from app.database import init_db
from database_creator import create_database_if_not_exists
from brand_initializer import initialize_brand_summaries

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Database Setup')
    parser.add_argument('--db-password', type=str, required=True, help='Database password')
    return parser.parse_args()


def main():
    """Main function to initialize the database."""
    # Parse command line arguments
    args = parse_arguments()
    
    logger.info("Starting database initialization...")
    
    try:
        # Create database if it doesn't exist
        create_database_if_not_exists(args.db_password)
        
        # Initialize tables
        init_db(args.db_password)
        logger.info("Database tables created successfully")
        
        # Initialize brand summaries
        initialize_brand_summaries(args.db_password)
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.error("Please check your database connection and try again")


if __name__ == "__main__":
    main() 