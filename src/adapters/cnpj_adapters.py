import httpx
from typing import Optional, Dict, Any
from src.adapters.interfaces import CNPJAdapterInterface
from src.models.schemas import CompanyData


class BrasilAPICNPJAdapter(CNPJAdapterInterface):
    def __init__(self, base_url: Optional[str] = None):
        from src.config.settings import settings
        self.base_url = base_url or settings.BRASILAPI_BASE_URL

    async def get_company_data(self, cnpj: str) -> Optional[CompanyData]:
        from src.config.settings import settings
        url = f"{self.base_url}/api/cnpj/v1/{cnpj}"
        
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            try:
                response = await client.get(url, headers={"User-Agent": settings.USER_AGENT})
                response.raise_for_status()
                data = response.json()
                
                return CompanyData(
                    cnpj=data.get("cnpj", ""),
                    razao_social=data.get("razao_social", ""),
                    nome_fantasia=data.get("nome_fantasia"),
                    uf=data.get("uf", ""),
                    municipio=data.get("municipio", ""),
                    logradouro=data.get("logradouro", ""),
                    bairro=data.get("bairro"),
                    cep=data.get("cep", ""),
                    numero=data.get("numero"),
                    complemento=data.get("complemento")
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