"""
API endpoints for brand mentions.
"""
from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
import logging

from .models import BrandMention

logger = logging.getLogger(__name__)


def get_db_dependency(password: str):
    """Create database dependency with password."""
    from .database import get_db
    return lambda: next(get_db(password))


async def root():
    """Root endpoint with API information."""
    return {
        "message": "Brand Mentions API",
        "version": "1.0.0",
        "endpoints": {
            "GET /mentions": "Get total mentions for all brands",
            "GET /mentions/{brand}": "Get mentions for a specific brand"
        }
    }


async def favicon():
    """Handle favicon requests to prevent 404 errors."""
    return Response(status_code=204)  # No content response


async def get_mentions(db: Session) -> Dict[str, int]:
    """Get total mentions for all brands."""
    try:
        results = db.query(
            BrandMention.brand_name,
            func.sum(BrandMention.mention_count).label('total_mentions')
        ).group_by(BrandMention.brand_name).all()
        
        mentions = {result.brand_name: result.total_mentions for result in results}
        
        # Ensure all brands are present (even with 0 mentions)
        all_brands = ['nike', 'adidas', 'hoka', 'new balance', 'jordan']
        for brand in all_brands:
            if brand not in mentions:
                mentions[brand] = 0
        
        return mentions
        
    except Exception as e:
        logger.error(f"Error retrieving mentions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def get_brand_mentions(brand: str, db: Session) -> Dict[str, Any]:
    """Get mentions for a specific brand."""
    try:
        brand_lower = brand.lower()
        
        result = db.query(
            func.sum(BrandMention.mention_count).label('total_mentions')
        ).filter(BrandMention.brand_name == brand_lower).scalar()
        
        total_mentions = result or 0
        
        return {
            "brand": brand_lower,
            "mentions": total_mentions
        }
        
    except Exception as e:
        logger.error(f"Error retrieving mentions for {brand}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}
