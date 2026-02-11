from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from src.services.validation_service import AddressValidationService
from src.models.schemas import ValidationResult, ValidationRequest
from src.utils.logging import setup_logging
from src.middleware.rate_limiter import rate_limiter

setup_logging()

app = FastAPI(
    title="Validação de Cadastro de Clientes",
    description="Microsserviço para validação de endereço de clientes usando CNPJ e CEP",
    version="1.0.0"
)

validation_service = AddressValidationService()


@app.post("/validate", response_model=ValidationResult, status_code=status.HTTP_200_OK)
async def validate_customer_address(request: ValidationRequest):
    try:
        result = await validation_service.validate_customer_address(
            cnpj=request.cnpj,
            cep=request.cep
        )
        
        if result.valid:
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Comprehensive health check including dependencies"""
    from src.utils.health import health_checker
    return await health_checker.comprehensive_health_check()