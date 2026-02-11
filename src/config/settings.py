import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API URLs
    BRASILAPI_BASE_URL: str = os.getenv("BRASILAPI_BASE_URL", "https://brasilapi.com.br")
    VIACEP_BASE_URL: str = os.getenv("VIACEP_BASE_URL", "https://viacep.com.br")
    
    # Timeouts
    HTTP_TIMEOUT: float = float(os.getenv("HTTP_TIMEOUT", "10.0"))
    
    # Retry Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "1.0"))
    
    # Circuit Breaker Configuration
    FAILURE_THRESHOLD: int = int(os.getenv("FAILURE_THRESHOLD", "5"))
    RECOVERY_TIMEOUT: int = int(os.getenv("RECOVERY_TIMEOUT", "60"))
    
    # Service Configuration
    CEP_MAX_RETRIES: int = int(os.getenv("CEP_MAX_RETRIES", "3"))
    
    # User Agent
    USER_AGENT: str = os.getenv("USER_AGENT", "address-validation-service/1.0")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True


settings = Settings()