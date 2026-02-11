from typing import Optional
import re
import asyncio
from src.adapters.cnpj_adapters import BrasilAPICNPJAdapter
from src.strategies.cep_strategy import CEPProviderStrategy
from src.strategies.resilience_simple import retry_simple as retry, SimpleCircuitBreaker as CircuitBreaker, with_simple_circuit_breaker as with_circuit_breaker
from src.models.schemas import CompanyData, AddressData, ValidationResult
from src.utils.logging import get_logger


class AddressValidationService:
    def __init__(self):
        from src.config.settings import settings
        self.logger = get_logger("AddressValidationService")
        self.cnpj_adapter = BrasilAPICNPJAdapter()
        self.cep_strategy = CEPProviderStrategy()
        self.cnpj_circuit_breaker = CircuitBreaker(
            failure_threshold=settings.FAILURE_THRESHOLD, 
            recovery_timeout=settings.RECOVERY_TIMEOUT
        )
        self.cep_circuit_breaker = CircuitBreaker(
            failure_threshold=settings.FAILURE_THRESHOLD, 
            recovery_timeout=settings.RECOVERY_TIMEOUT
        )

    async def get_company_data(self, cnpj: str) -> Optional[CompanyData]:
        from src.config.settings import settings
        clean_cnpj = re.sub(r'[^\d]', '', cnpj)
        return await self.cnpj_adapter.get_company_data(clean_cnpj)

    async def get_address_data(self, cep: str) -> Optional[AddressData]:
        from src.config.settings import settings
        clean_cep = re.sub(r'[^\d]', '', cep)
        return await self.cep_strategy.get_address_data(clean_cep)

    def _normalize_string(self, text: str) -> str:
        if not text:
            return ""
        return re.sub(r'[^\w\s]', '', text.upper().strip())

    def _validate_address_match(self, company_data: CompanyData, address_data: AddressData) -> bool:
        company_state = self._normalize_string(company_data.uf)
        address_state = self._normalize_string(address_data.state)
        
        company_city = self._normalize_string(company_data.municipio)
        address_city = self._normalize_string(address_data.city)
        
        company_street = self._normalize_string(company_data.logradouro)
        address_street = self._normalize_string(address_data.street or "")
        
        state_match = company_state == address_state
        city_match = company_city == address_city
        
        street_match = False
        if company_street and address_street:
            street_match = (
                company_street in address_street or 
                address_street in company_street
            )
        
        return state_match and city_match and street_match

    async def validate_customer_address(self, cnpj: str, cep: str) -> ValidationResult:
        self.logger.info(f"Iniciando validação para CNPJ: {cnpj}, CEP: {cep}")
        
        try:
            # Executar consultas em PARALELO
            company_task = self.get_company_data(cnpj)
            address_task = self.get_address_data(cep)
            
            company_data, address_data = await asyncio.gather(
                company_task, 
                address_task,
                return_exceptions=True
            )
            
            # Tratar exceções se houver
            if isinstance(company_data, Exception):
                self.logger.error(f"Erro na consulta CNPJ: {str(company_data)}")
                company_data = None
            
            if isinstance(address_data, Exception):
                self.logger.error(f"Erro na consulta CEP: {str(address_data)}")
                address_data = None
            
            # Validar resultados
            if not company_data:
                self.logger.warning(f"Empresa não encontrada para CNPJ: {cnpj}")
                return ValidationResult(
                    valid=False,
                    message="Empresa não encontrada",
                    company_data=None,
                    address_data=None
                )

            if not address_data:
                self.logger.warning(f"Endereço não encontrado para CEP: {cep}")
                return ValidationResult(
                    valid=False,
                    message="Endereço não encontrado",
                    company_data=company_data,
                    address_data=None
                )

            is_valid = self._validate_address_match(company_data, address_data)
            
            if is_valid:
                self.logger.info("Validação de endereço bem-sucedida")
                return ValidationResult(
                    valid=True,
                    message="Endereço validado com sucesso",
                    company_data=company_data,
                    address_data=address_data
                )
            else:
                self.logger.info("Endereço não corresponde ao da empresa")
                return ValidationResult(
                    valid=False,
                    message="Endereço não corresponde ao da empresa",
                    company_data=company_data,
                    address_data=address_data
                )
                
        except Exception as e:
            self.logger.error(f"Erro na validação: {str(e)}")
            return ValidationResult(
                valid=False,
                message=f"Erro na validação: {str(e)}",
                company_data=None,
                address_data=None
            )