import pytest
import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Async test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Test data fixtures
@pytest.fixture
def valid_cnpj():
    return "00924432000199"

@pytest.fixture
def invalid_cnpj():
    return "11111111111111"

@pytest.fixture
def valid_cep():
    return "13288390"

@pytest.fixture
def invalid_cep():
    return "00000000"

@pytest.fixture
def sample_validation_request():
    return {
        "cnpj": "00924432000199",
        "cep": "13288390"
    }

@pytest.fixture
def sample_validation_request_invalid():
    return {
        "cnpj": "11111111111111",
        "cep": "13288390"
    }

# Mock fixtures for integration tests
@pytest.fixture
def mock_company_data():
    from src.models.schemas import CompanyData
    return CompanyData(
        cnpj="00924432000199",
        razao_social="Test Company",
        nome_fantasia="Test Co.",
        uf="SP",
        municipio="Test City",
        logradouro="Test Street",
        bairro="Test Neighborhood",
        cep="13288390",
        numero="123",
        complemento=None
    )

@pytest.fixture
def mock_address_data():
    from src.models.schemas import AddressData
    return AddressData(
        cep="13288390",
        state="SP",
        city="Test City",
        neighborhood="Test Neighborhood",
        street="Test Street",
        service="test_service"
    )

# HTTP client fixtures
@pytest.fixture
def test_client():
    """FastAPI test client fixture"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)

@pytest.fixture
def http_client():
    """HTTP client for contract tests"""
    import httpx
    return httpx.Client(timeout=10.0)

# Mock response fixtures
@pytest.fixture
def mock_brasilapi_cnpj_response():
    return {
        "cnpj": "00924432000199",
        "razao_social": "Test Company",
        "nome_fantasia": "Test Co.",
        "uf": "SP",
        "municipio": "Test City",
        "logradouro": "Test Street",
        "bairro": "Test Neighborhood",
        "cep": "13288390",
        "numero": "123",
        "complemento": None
    }

@pytest.fixture
def mock_brasilapi_cep_response():
    return {
        "cep": "13288390",
        "state": "SP",
        "city": "Test City",
        "neighborhood": "Test Neighborhood",
        "street": "Test Street",
        "service": "brasilapi"
    }

@pytest.fixture
def mock_viacep_response():
    return {
        "cep": "13288-390",
        "logradouro": "Test Street",
        "complemento": "",
        "bairro": "Test Neighborhood",
        "localidade": "Test City",
        "uf": "SP",
        "ibge": "1234567",
        "gia": "1234",
        "ddd": "19",
        "siafi": "1234"
    }

# Service fixtures
@pytest.fixture
async def validation_service():
    """Validation service fixture"""
    from src.services.validation_service import AddressValidationService
    service = AddressValidationService()
    # Clear cache for clean state
    from src.utils.cache import cache
    await cache.clear()
    return service

@pytest.fixture
async def cache_instance():
    """Cache instance fixture"""
    from src.utils.cache import ThreadSafeCache
    cache = ThreadSafeCache(max_size=10, ttl=1)
    await cache.clear()
    return cache

@pytest.fixture
def circuit_breaker():
    """Circuit breaker fixture"""
    from src.strategies.resilience import CircuitBreaker
    return CircuitBreaker(failure_threshold=3, recovery_timeout=1)

# Environment fixtures
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    test_vars = {
        "HTTP_TIMEOUT": "5.0",
        "CACHE_TTL": "60",
        "LOG_LEVEL": "DEBUG",
        "FAILURE_THRESHOLD": "3",
        "RECOVERY_TIMEOUT": "30"
    }
    
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
    
    return test_vars

# Logging fixtures
@pytest.fixture
def capture_logs(caplog):
    """Fixture to capture log outputs"""
    import logging
    caplog.set_level(logging.INFO)
    return caplog