"""
FastAPI application with brand mention endpoints.
"""
from fastapi import FastAPI, Depends
import logging

from .database import init_db
from .endpoints import (
    root, favicon, get_mentions, get_brand_mentions, 
    health_check, get_db_dependency
)
from config import DEBUG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(password: str):
    """Create FastAPI app with password."""
    app = FastAPI(
        title="Brand Mentions API",
        description="API for retrieving brand mention metrics from ChatGPT responses",
        version="1.0.0",
        debug=DEBUG
    )

    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        """Initialize database tables on startup."""
        init_db(password)
        logger.info("Database initialized successfully")

    # Create database dependency
    db_dependency = get_db_dependency(password)

    # Register endpoints
    @app.get("/")
    async def root_endpoint():
        return await root()

    @app.get("/favicon.ico")
    async def favicon_endpoint():
        return await favicon()

    @app.get("/mentions")
    async def mentions_endpoint(db=Depends(db_dependency)):
        return await get_mentions(db)

    @app.get("/mentions/{brand}")
    async def brand_mentions_endpoint(brand: str, db=Depends(db_dependency)):
        return await get_brand_mentions(brand, db)

    @app.get("/health")
    async def health_endpoint():
        return await health_check()

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app("password"), host="0.0.0.0", port=8000) 