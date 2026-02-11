# Serviço de Validação de Endereço de Clientes

> **Questão 1** - Microsserviço para validação cadastral via CNPJ e CEP [Desafios](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/challenge.md)


## 📋 Preview do Desafio 01

### 🎯 **Objetivo**
Validar se o endereço de cadastro do cliente corresponde aos dados oficiais da empresa, comparando informações obtidas via **CNPJ** e **CEP**.

### ⚡ **Como Funciona**
1. **Recebe**: CNPJ + CEP via POST `/validate`
2. **Consulta Paralela**: 
   - **BrasilAPI** → Dados da empresa (CNPJ)
   - **BrasilAPI** → Endereço (CEP)
   - **ViaCEP** → Endereço (fallback após 3 tentativas)
3. **Compara**: UF, cidade e logradouro
4. **Retorna**: 
   - ✅ **HTTP 200** → Endereços correspondem
   - ❌ **HTTP 404** → Endereços não correspondem

### 📊 **Performance**
- **Tempo Resposta**: ~300ms (consultas paralelas)
- **Resiliência**: Circuit breaker + retentativas
- **Disponibilidade**: Health check automático
- **Testes**: 30 casos cobrindo todos os cenários

---

## 🚀 Como Rodar o Projeto

### 📋 **Pré-requisitos**
- Docker e Docker Compose instalados
- Git para clonar o repositório

### 🐳 **Opção 1: Docker (Recomendado)**

```bash
# 1. Clonar o repositório
git clone <repository-url>
cd questao01

# 2. Configurar ambiente (opcional)
cp .env.example .env
# Editar .env se necessário

# 3. Subir containers
docker-compose up --build -d

# 4. Verificar logs
docker-compose logs -f address_validation_api

# 5. Testar API
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"cnpj": "17322527000135", "cep": "67105070"}'

# 6. Health check
curl http://localhost:8000/health
```

### 💻 **Opção 2: Local Development**

```bash
# 1. Clonar e entrar no diretório
git clone <repository-url>
cd questao01

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar ambiente
cp .env.example .env

# 5. Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🛠️ Tecnologias e Padrões Utilizados

Para o desenvolvimento deste projeto, as seguintes tecnologias e padrões foram utilizados:

### ⚙️ **Tecnologias**

#### **Backend**
- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web moderno e assíncrono
- **Uvicorn** - Servidor ASGI para FastAPI
- **Pydantic** - Validação de dados e serialização
- **httpx** - Cliente HTTP assíncrono

#### **Infraestrutura**
- **Docker** - Containerização da aplicação
- **Docker Compose** - Orquestração de containers

#### **Testes**
- **pytest** - Framework de testes
- **pytest-cov** - Cobertura de código
- **pytest-asyncio** - Suporte a testes assíncronos

#### **Monitoramento e Logging**
- **Python Logging** - Logs estruturados
- **Health Check** - Verificação de saúde do serviço

### 🏗️ **Design Patterns**

#### **Arquitetural**
- **Hexagonal Architecture (Ports and Adapters)** - Isola domínio de infraestrutura
- **Microservices** - Serviço independente e especializado

#### **Comportamentais**
- **Strategy Pattern** - Chaveamento entre provedores CEP
- **Circuit Breaker Pattern** - Proteção contra falhas em cascata
- **Decorator Pattern** - Adição de retry e logging

#### **Estruturais**
- **Adapter Pattern** - Padronização das diferentes APIs externas
- **Singleton Pattern** - Configurações centralizadas (settings)

### 📋 **Princípios SOLID**

- **S** - Single Responsibility: Cada classe com uma responsabilidade única
- **O** - Open/Closed: Aberto para extensão, fechado para modificação
- **L** - Liskov Substitution: Implementações substituíveis por interfaces
- **I** - Interface Segregation: Interfaces específicas e coesas
- **D** - Dependency Inversion: Dependência de abstrações, não concretizações

### 🔧 **Técnicas e Boas Práticas**

#### **Performance**
- **Consultas Paralelas** - `asyncio.gather()` para CNPJ e CEP simultâneos
- **Timeouts Configuráveis** - Prevenção de lentidão
- **Resposta Síncrona** - Conforme requisito da Questão 1

#### **Resiliência**
- **Retentativas Automáticas** - Com backoff exponencial
- **Circuit Breaker** - Abertura automática em falhas
- **Fallback Automático** - BrasilAPI → ViaCEP após 3 tentativas
- **Graceful Degradation** - Status degradado em health check

#### **Qualidade**
- **Type Hints** - Python type annotations
- **Validação de Entrada** - Formato CNPJ/CEP
- **Logging Estruturado** - Níveis (DEBUG, INFO, WARNING, ERROR)
- **Rate Limiting** - Proteção contra abuso
- **Health Check** - Monitoramento de dependências

#### **Testes**
- **Test Pirâmide** - Unitários → Integração → Contratos
- **30 Casos de Teste** - Cobertura completa
- **Mocking** - Isolamento de dependências externas
- **Testes Assíncronos** - Suporte a async/await

### 🌐 **APIs Externas**

#### **BrasilAPI**
- **CNPJ**: `https://brasilapi.com.br/api/cnpj/v1/{cnpj}`
- **CEP**: `https://brasilapi.com.br/api/cep/v2/{cep}`
- **Status**: Primário, fallback após 3 tentativas

#### **ViaCEP**
- **CEP**: `https://viacep.com.br/ws/{cep}/json/`
- **Status**: Provedor alternativo (backup)

---

## 🧪 Como Rodar os Testes

### 🐳 **Testes via Docker**

```bash
# 1. Build da imagem com testes
docker-compose build

# 2. Executar todos os testes
docker-compose run --rm api python -m pytest tests/ -v

# 3. Executar testes específicos
docker-compose run --rm api python -m pytest tests/unit/ -v
docker-compose run --rm api python -m pytest tests/integration/ -v
docker-compose run --rm api python -m pytest tests/contracts/ -v

# 4. Verificar cobertura
docker-compose run --rm api python -m pytest tests/ --cov=src --cov-report=html
```

### 💻 **Testes Local**

```bash
# 1. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Instalar dependências de teste
pip install pytest pytest-cov pytest-asyncio httpx

# 3. Executar todos os testes
python -m pytest tests/ -v

# 4. Executar por categoria
python -m pytest tests/unit/ -v              # Unitários
python -m pytest tests/integration/ -v        # Integração
python -m pytest tests/contracts/ -v          # Contratos APIs

# 5. Gerar relatório de cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📁 Estrutura do Projeto

```
questao01/
├── 📁 src/
│   ├── 📁 adapters/           # Implementações APIs externas
│   │   ├── cnpj_adapters.py  # BrasilAPI CNPJ
│   │   ├── cep_adapters.py   # BrasilAPI + ViaCEP
│   │   └── interfaces.py     # Contratos das APIs
│   ├── 📁 strategies/        # Padrões de projeto
│   │   ├── cep_strategy.py   # Strategy CEP providers
│   │   └── resilience.py    # Circuit breaker + retry
│   ├── 📁 services/         # Lógica de negócio
│   │   └── validation_service.py
│   ├── 📁 models/           # Data models
│   │   └── schemas.py
│   ├── 📁 utils/            # Utilitários
│   │   ├── logging.py
│   │   └── validators.py
│   ├── 📁 config/           # Configurações
│   │   └── settings.py
│   └── 📁 middleware/       # FastAPI middleware
│       └── rate_limiter.py
├── 📁 tests/               # Suíte de testes
│   ├── 📁 unit/            # Testes unitários
│   ├── 📁 integration/      # Testes integração
│   ├── 📁 contracts/       # Testes contratos APIs
│   └── conftest.py         # Config pytest
├── 📁 docs/                # Documentação
├── 📄 main.py              # FastAPI application
├── 📄 requirements.txt     # Dependências Python
├── 📄 docker-compose.yml    # Orquestração containers
├── 📄 Dockerfile          # Build da aplicação
├── 📄 .env.example        # Variáveis ambiente
├── 📄 .gitignore         # Git ignore
└── 📄 README.md           # Este arquivo
```

---

## 🎯 Exemplos de Uso

### ✅ **Request Bem-Sucedido**

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "17322527000135",
    "cep": "67105070"
  }'

# Resposta: HTTP 200
{
  "valid": true,
  "message": "Endereço validado com sucesso",
  "company_data": {
    "cnpj": "17322527000135",
    "razao_social": "S D ALFAIA TURISMO",
    "uf": "PA",
    "municipio": "ANANINDEUA",
    "logradouro": "URIBOCA VELHA"
  },
  "address_data": {
    "cep": "67105070",
    "state": "PA", 
    "city": "Ananindeua",
    "street": "Rua Uriboca Velha"
  }
}
```

### ❌ **Request Não Correspondente**

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "00924432000199",
    "cep": "13288390"
  }'

# Resposta: HTTP 404
{
  "detail": "Endereço não corresponde ao da empresa"
}
```

---

## 🔧 Configuração

### 📋 **Variáveis de Ambiente**

```bash
# .env
BRASILAPI_BASE_URL=https://brasilapi.com.br
VIACEP_BASE_URL=https://viacep.com.br
HTTP_TIMEOUT=5.0
MAX_RETRIES=2
RETRY_DELAY=0.5
FAILURE_THRESHOLD=3
RECOVERY_TIMEOUT=30
LOG_LEVEL=INFO
USER_AGENT=address-validation-service/1.0
CEP_MAX_RETRIES=3
```
