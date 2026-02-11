import httpx
from typing import Optional, Dict, Any
from src.adapters.interfaces import CEPAdapterInterface
from src.models.schemas import AddressData


class BrasilAPICEPAdapter(CEPAdapterInterface):
    def __init__(self, base_url: Optional[str] = None):
        from src.config.settings import settings
        self.base_url = base_url or settings.BRASILAPI_BASE_URL

    async def get_address_data(self, cep: str) -> Optional[AddressData]:
        from src.config.settings import settings
        clean_cep = cep.replace("-", "").replace(".", "")
        url = f"{self.base_url}/api/cep/v2/{clean_cep}"
        
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            try:
                response = await client.get(url, headers={"User-Agent": settings.USER_AGENT})
                response.raise_for_status()
                data = response.json()
                
                return AddressData(
                    cep=data.get("cep", ""),
                    state=data.get("state", ""),
                    city=data.get("city", ""),
                    neighborhood=data.get("neighborhood"),
                    street=data.get("street"),
                    service=data.get("service", "brasilapi")
                )
            except httpx.TimeoutException:
                return None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
            except httpx.HTTPError:
                return None
            except Exception:
                return None


class ViaCEPAdapter(CEPAdapterInterface):
    def __init__(self, base_url: Optional[str] = None):
        from src.config.settings import settings
        self.base_url = base_url or settings.VIACEP_BASE_URL

    async def get_address_data(self, cep: str) -> Optional[AddressData]:
        from src.config.settings import settings
        clean_cep = cep.replace("-", "").replace(".", "")
        url = f"{self.base_url}/ws/{clean_cep}/json/"
        
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            try:
                response = await client.get(url, headers={"User-Agent": settings.USER_AGENT})
                response.raise_for_status()
                data = response.json()
                
                if "erro" in data:
                    return None
                    
                return AddressData(
                    cep=data.get("cep", ""),
                    state=data.get("uf", ""),
                    city=data.get("localidade", ""),
                    neighborhood=data.get("bairro"),
                    street=data.get("logradouro"),
                    service="viacep"
                )
            except httpx.TimeoutException:
                return None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
            except httpx.HTTPError:
                return None
            except Exception:
                return None