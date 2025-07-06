"""
Tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.api import create_app
from app.database import get_db, init_db
from app.models import Prompt, BrandMention

# Create test app with test password
test_app = create_app("test_password")
client = TestClient(test_app)


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Initialize test database
    init_db("test_password")
    yield
    # Cleanup would go here in a real implementation


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Brand Mentions API"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_mentions_endpoint():
    """Test the mentions endpoint."""
    response = client.get("/mentions")
    assert response.status_code == 200
    data = response.json()
    
    # Check that all expected brands are present
    expected_brands = ['nike', 'adidas', 'hoka', 'new balance', 'jordan']
    for brand in expected_brands:
        assert brand in data
        assert isinstance(data[brand], int)


def test_brand_mentions_endpoint():
    """Test the specific brand mentions endpoint."""
    response = client.get("/mentions/nike")
    assert response.status_code == 200
    data = response.json()
    
    assert "brand" in data
    assert "mentions" in data
    assert data["brand"] == "nike"
    assert isinstance(data["mentions"], int)


def test_brand_mentions_case_insensitive():
    """Test that brand names are case insensitive."""
    response = client.get("/mentions/NIKE")
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "nike"


def test_invalid_brand():
    """Test with an invalid brand name."""
    response = client.get("/mentions/invalid_brand")
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "invalid_brand"
    assert data["mentions"] == 0 