import re
from typing import Optional


def validate_cnpj(cnpj: str) -> tuple[bool, Optional[str]]:
    """
    Valida formato e dígitos verificadores do CNPJ
    
    Args:
        cnpj: CNPJ para validação (pode conter pontuação)
    
    Returns:
        tuple[bool, Optional[str]]: (é_valido, mensagem_erro)
    """
    # Remove caracteres não numéricos
    cnpj_clean = re.sub(r'[^\d]', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj_clean) != 14:
        return False, "CNPJ deve conter 14 dígitos"
    
    # Verifica se todos os dígitos são iguais (inválido)
    if cnpj_clean == cnpj_clean[0] * 14:
        return False, "CNPJ com todos os dígitos iguais é inválido"
    
    # Calcula dígitos verificadores
    def calculate_digit(cnpj_numbers: list[int], weights: list[int]) -> int:
        total = sum(num * weight for num, weight in zip(cnpj_numbers, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Pesos para o primeiro dígito verificador
    weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Pesos para o segundo dígito verificador
    weights_second = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Converte para lista de inteiros
    cnpj_numbers = [int(d) for d in cnpj_clean]
    
    # Calcula primeiro dígito verificador
    calculated_first = calculate_digit(cnpj_numbers[:12], weights_first)
    expected_first = cnpj_numbers[12]
    
    if calculated_first != expected_first:
        return False, "Primeiro dígito verificador do CNPJ é inválido"
    
    # Calcula segundo dígito verificador
    calculated_second = calculate_digit(cnpj_numbers[:13], weights_second)
    expected_second = cnpj_numbers[13]
    
    if calculated_second != expected_second:
        return False, "Segundo dígito verificador do CNPJ é inválido"
    
    return True, None


def validate_cep(cep: str) -> tuple[bool, Optional[str]]:
    """
    Valida formato do CEP
    
    Args:
        cep: CEP para validação (pode conter pontuação)
    
    Returns:
        tuple[bool, Optional[str]]: (é_valido, mensagem_erro)
    """
    # Remove caracteres não numéricos
    cep_clean = re.sub(r'[^\d]', '', cep)
    
    # Verifica se tem 8 dígitos
    if len(cep_clean) != 8:
        return False, "CEP deve conter 8 dígitos"
    
    # Verifica se todos os dígitos são iguais (inválido)
    if cep_clean == cep_clean[0] * 8:
        return False, "CEP com todos os dígitos iguais é inválido"
    
    return True, None


def format_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX
    
    Args:
        cnpj: CNPJ sem formatação
    
    Returns:
        str: CNPJ formatado
    """
    cnpj_clean = re.sub(r'[^\d]', '', cnpj)
    if len(cnpj_clean) != 14:
        return cnpj
    
    return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:]}"


def format_cep(cep: str) -> str:
    """
    Formata CEP no padrão XXXXX-XXX
    
    Args:
        cep: CEP sem formatação
    
    Returns:
        str: CEP formatado
    """
    cep_clean = re.sub(r'[^\d]', '', cep)
    if len(cep_clean) != 8:
        return cep
    
    return f"{cep_clean[:5]}-{cep_clean[5:]}"