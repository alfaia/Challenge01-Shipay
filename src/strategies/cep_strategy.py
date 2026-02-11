from typing import List, Optional
from src.adapters.interfaces import CEPAdapterInterface
from src.adapters.cep_adapters import BrasilAPICEPAdapter, ViaCEPAdapter
from src.models.schemas import AddressData


class CEPProviderStrategy:
    def __init__(self, max_retries: Optional[int] = None):
        from src.config.settings import settings
        self.providers: List[CEPAdapterInterface] = [
            BrasilAPICEPAdapter(),
            ViaCEPAdapter()
        ]
        self.max_retries = max_retries or settings.CEP_MAX_RETRIES

    async def get_address_data(self, cep: str) -> Optional[AddressData]:
        for provider_index, provider in enumerate(self.providers):
            for attempt in range(self.max_retries):
                try:
                    result = await provider.get_address_data(cep)
                    if result:
                        return result
                except Exception:
                    if attempt == self.max_retries - 1:
                        break
                    continue
            
            if provider_index < len(self.providers) - 1:
                continue
                
        return None

    def set_providers(self, providers: List[CEPAdapterInterface]):
        self.providers = providers