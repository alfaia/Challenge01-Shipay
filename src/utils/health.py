import asyncio
import httpx
from typing import Dict, Any
from src.config.settings import settings


class HealthChecker:
    def __init__(self):
        self.timeout = 5.0  # Health check timeout
    
    async def check_brasilapi(self) -> Dict[str, Any]:
        """Check BrasilAPI health"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{settings.BRASILAPI_BASE_URL}/api/cnpj/v1/00000000000000")
                return {
                    "status": "healthy" if response.status_code in [200, 404] else "unhealthy",
                    "response_time_ms": response.elapsed.total_seconds() * 1000 if hasattr(response, 'elapsed') else None,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_viacep(self) -> Dict[str, Any]:
        """Check ViaCEP health"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{settings.VIACEP_BASE_URL}/ws/00000000/json/")
                return {
                    "status": "healthy" if response.status_code in [200, 400] else "unhealthy",
                    "response_time_ms": response.elapsed.total_seconds() * 1000 if hasattr(response, 'elapsed') else None,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_cache(self) -> Dict[str, Any]:
        """Check cache functionality"""
        try:
            from src.utils.cache import cache
            cache_size = cache.size()
            
            return {
                "status": "healthy",
                "cache_size": cache_size,
                "max_size": cache.max_size
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def check_circuit_breakers(self) -> Dict[str, Any]:
        """Check circuit breaker states"""
        try:
            from src.services.validation_service import AddressValidationService
            service = AddressValidationService()
            
            return {
                "status": "healthy",
                "cnpj_circuit_breaker": {
                    "state": service.cnpj_circuit_breaker.state,
                    "failure_count": service.cnpj_circuit_breaker.failure_count,
                    "threshold": service.cnpj_circuit_breaker.failure_threshold
                },
                "cep_circuit_breaker": {
                    "state": service.cep_circuit_breaker.state,
                    "failure_count": service.cep_circuit_breaker.failure_count,
                    "threshold": service.cep_circuit_breaker.failure_threshold
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Run all health checks"""
        checks = {
            "service": {"status": "healthy", "message": "Address validation service is running"},
            "brasilapi": await self.check_brasilapi(),
            "viacep": await self.check_viacep(),
            "cache": await self.check_cache(),
            "circuit_breakers": await self.check_circuit_breakers()
        }
        
        # Determine overall health
        overall_status = "healthy"
        unhealthy_services = []
        
        for service_name, result in checks.items():
            if service_name == "service":
                continue
            if result.get("status") == "unhealthy":
                overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
                unhealthy_services.append(service_name)
        
        return {
            "status": overall_status,
            "timestamp": asyncio.get_event_loop().time(),
            "checks": checks,
            "unhealthy_services": unhealthy_services
        }


health_checker = HealthChecker()