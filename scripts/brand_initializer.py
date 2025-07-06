"""
Brand initialization functionality.
"""
import logging
from app.database import create_engine_with_password
from app.models import BrandSummary
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def initialize_brand_summaries(password: str):
    """Initialize brand summary records."""
    try:
        engine = create_engine_with_password(password)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Define initial brands
        brands = ['nike', 'adidas', 'hoka', 'new balance', 'jordan']
        
        for brand in brands:
            # Check if brand summary exists
            existing = db.query(BrandSummary).filter(BrandSummary.brand_name == brand).first()
            
            if not existing:
                # Create new brand summary
                brand_summary = BrandSummary(
                    brand_name=brand,
                    total_mentions=0
                )
                db.add(brand_summary)
                logger.info(f"Created brand summary for: {brand}")
        
        db.commit()
        logger.info("Brand summaries initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing brand summaries: {e}")
        db.rollback()
    finally:
        db.close() 