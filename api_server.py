#!/usr/bin/env python3
"""
Stage 2: API Server
FastAPI server for retrieving brand mention metrics.
"""
import uvicorn
import logging
import argparse
import socket
from app.api import create_app
from app.database import init_db
from config import API_HOST, API_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def is_port_in_use(port: int) -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except OSError:
            return True


def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    for i in range(max_attempts):
        port = start_port + i
        if not is_port_in_use(port):
            return port
    raise RuntimeError(f"Could not find an available port in range {start_port}-{start_port + max_attempts - 1}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Brand Mentions API Server')
    parser.add_argument('--db-password', type=str, required=True, help='Database password')
    parser.add_argument('--host', type=str, default=API_HOST, help='API host')
    parser.add_argument('--port', type=int, default=API_PORT, help='API port')
    parser.add_argument('--no-auto-port', action='store_true', help='Disable automatic port finding')
    return parser.parse_args()


def main():
    """Main function to run the API server."""
    # Parse command line arguments
    args = parse_arguments()
    
    logger.info("Starting Brand Mentions API Server (Stage 2)")
    
    # Initialize database
    init_db(args.db_password)
    logger.info("Database initialized")
    
    # Create FastAPI app with password
    app = create_app(args.db_password)
    
    # Find available port if auto-port is enabled
    if not args.no_auto_port:
        try:
            port = find_available_port(args.port)
            if port != args.port:
                logger.info(f"Port {args.port} is in use, using port {port} instead")
        except RuntimeError as e:
            logger.error(f"Port finding failed: {e}")
            port = args.port
    else:
        port = args.port
    
    # Run the server
    logger.info(f"Starting server on {args.host}:{port}")
    uvicorn.run(
        app,
        host=args.host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main() 