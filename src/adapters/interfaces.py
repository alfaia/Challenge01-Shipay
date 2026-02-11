from abc import ABC, abstractmethod
from typing import Optional
from src.models.schemas import CompanyData, AddressData


class CNPJAdapterInterface(ABC):
    @abstractmethod
    async def get_company_data(self, cnpj: str) -> Optional[CompanyData]:
        pass


class CEPAdapterInterface(ABC):
    @abstractmethod
    async def get_address_data(self, cep: str) -> Optional[AddressData]:
        pass