from typing import Optional
from pydantic import BaseModel, field_validator
from src.utils.validators import validate_cnpj, validate_cep


class CompanyData(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    uf: str
    municipio: str
    logradouro: str
    bairro: Optional[str] = None
    cep: str
    numero: Optional[str] = None
    complemento: Optional[str] = None


class AddressData(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    service: Optional[str] = None


class ValidationResult(BaseModel):
    valid: bool
    message: str
    company_data: Optional[CompanyData]
    address_data: Optional[AddressData]


class ValidationRequest(BaseModel):
    cnpj: str
    cep: str
    
    @field_validator('cnpj')
    @classmethod
    def validate_cnpj_format(cls, v):
        is_valid, error_msg = validate_cnpj(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @field_validator('cep')
    @classmethod
    def validate_cep_format(cls, v):
        is_valid, error_msg = validate_cep(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v