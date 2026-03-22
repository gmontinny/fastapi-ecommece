# FastAPI E-Commerce API

Uma API robusta e escalável para e-commerce desenvolvida com **FastAPI**, focada em boas práticas de programação, segurança com JWT e arquitetura modular.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy 2.0**: ORM para interação com o banco de dados.
- **Alembic**: Ferramenta de migrações para o banco de dados.
- **Pydantic V2**: Validação de dados e configurações via variáveis de ambiente.
- **Mensagens de Erro Customizadas**: Validações automáticas traduzidas para Português do Brasil (pt-BR).
- **JWT (JSON Web Token)**: Autenticação e autorização segura com suporte a Access e Refresh Tokens.
- **Slowapi**: Implementação de Rate Limiting.
- **HTTPX**: Cliente HTTP assíncrono para consumo de APIs externas (ViaCEP).
- **Docker & Docker Compose**: Containerização completa (App + DB).
- **Kubernetes**: Orquestração de containers com manifestos prontos para Deployment, Service e ConfigMaps.
- **Terraform (IaC)**: Infraestrutura como código para provisionamento automatizado na **AWS**, **Azure** e **GCP**.
- **Swagger UI & Redoc**: Documentação interativa e detalhada da API.

## 🏗️ Arquitetura do Projeto

O projeto segue o padrão **Repository Pattern** para desacoplar a lógica de negócio do acesso aos dados, facilitando a manutenção e testes.

### Estrutura de Pastas

```text
app/
├── api/             # Rotas da API (v1, v2...)
├── core/            # Configurações globais, segurança e envs
├── db/              # Sessão e conexão com banco de dados
├── models/          # Modelos SQLAlchemy (Entidades)
├── repository/      # Camada de abstração de acesso a dados
├── schemas/         # Modelos Pydantic (DTOs / Validações)
└── services/        # Integração com APIs externas (ViaCEP)
scripts/             # Scripts SQL de inicialização
alembic/             # Histórico e scripts de migração
docker-compose.yml   # Configuração do ambiente Docker
Dockerfile           # Definição da imagem da aplicação
requirements.txt     # Dependências do projeto
kubernetes/          # Manifestos para orquestração (Deployment, Service, Config)
terraform/           # Provisionamento de infraestrutura (AWS, Azure, GCP)
```

## 🛠️ Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados.

### Passos para rodar com Docker

1. **Clone o repositório** (ou copie os arquivos).
2. **Crie um arquivo `.env`** na raiz (baseado no `app/core/config.py` ou conforme solicitado):
   ```env
   POSTGRES_USER=gmontinny
   POSTGRES_PASSWORD=Gmontinny2026
   POSTGRES_DB=db
   POSTGRES_SERVER=db
   SECRET_KEY=sua_chave_secreta_aqui
   ```
3. **Suba os containers**:
   ```bash
   docker-compose up -d --build
   ```
4. **Acesse a documentação interativa**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### ☸️ Rodando com Kubernetes

O projeto já conta com manifestos para deploy em clusters Kubernetes.

1. **Configuração e Segredos**:
   ```bash
   kubectl apply -f kubernetes/config.yaml
   ```
2. **Banco de Dados (PostgreSQL)**:
   ```bash
   kubectl apply -f kubernetes/postgres.yaml
   ```
3. **Aplicação FastAPI**:
   ```bash
   kubectl apply -f kubernetes/app.yaml
   ```

### 🌍 Provisionamento com Terraform (IaC)

A infraestrutura pode ser provisionada automaticamente em qualquer um dos três principais provedores de nuvem:

- **AWS**: Localizado em `terraform/aws/` (EKS + RDS).
- **Azure**: Localizado em `terraform/azure/` (AKS + Azure Database for PostgreSQL).
- **GCP**: Localizado em `terraform/gcp/` (GKE + Cloud SQL).

Para usar, acesse a pasta do provedor desejado e execute:
```bash
terraform init
terraform plan
terraform apply
```

## 🏢 Entidades e Relacionamentos

A API agora suporta a gestão de:

- **Clientes (Customer)**: Dados pessoais e vínculos com múltiplos endereços.
- **Fornecedores (Supplier)**: Razão social, CNPJ e vínculos com múltiplos endereços.
- **Endereços (Address)**: Centralizados para clientes e fornecedores, com preenchimento automático via CEP.

### 🖼️ Diagrama de Entidade-Relacionamento (DER)

Abaixo está o diagrama que ilustra a estrutura do banco de dados e como as tabelas se relacionam. Note o uso de tabelas de associação para relacionamentos muitos-para-muitos (ex: categorias de produtos e tags) e chaves estrangeiras para vincular endereços a clientes ou fornecedores.

![Diagrama de Entidade-Relacionamento](der.png)

## 🌍 Integração com ViaCEP

O projeto utiliza um serviço assíncrono para consultar endereços brasileiros através da API do [ViaCEP](https://viacep.com.br/).

- Localização: `app/services/viacep.py`
- Utiliza a biblioteca `httpx` para chamadas não-bloqueantes.

## 🔒 Segurança e Rate Limiting

- **JWT**: Senhas são criptografadas com `bcrypt`. A API é protegida por autenticação JWT; os endpoints exigem que o token gerado seja enviado no cabeçalho `Authorization: Bearer <token>`. O sistema agora utiliza **Access Tokens** (curta duração) e **Refresh Tokens** (longa duração) para maior segurança.
- **Rate Limit**: Por padrão, o projeto possui limites de requisições configurados no `main.py` para evitar abusos nos endpoints.
- **Validação Localizada**: Todas as mensagens de erro de validação (campos obrigatórios, e-mails inválidos, formatos incorretos) são retornadas automaticamente em **Português do Brasil**.

## 📖 Guia de Uso da API

### 1. Autenticação e Autorização

Para acessar a maioria dos endpoints, você precisará estar autenticado.

#### Registrar Usuário
- **Endpoint**: `POST /auth/register`
- **Corpo da Requisição**:
  ```json
  {
    "email": "user@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "password": "senha_segura_123"
  }
  ```

#### Listar Usuários
- **Endpoint**: `GET /auth/users`
- **Requisito**: Requer Token JWT no cabeçalho.
- **Descrição**: Retorna a lista de todos os usuários registrados no sistema. Permite paginação via `skip` e `limit`.

#### Obter Usuário por ID
- **Endpoint**: `GET /auth/users/{user_id}`
- **Requisito**: Requer Token JWT no cabeçalho.
- **Descrição**: Retorna os detalhes de um usuário específico através do seu ID.

#### Atualizar Usuário
- **Endpoint**: `PUT /auth/users/{user_id}`
- **Requisito**: Requer Token JWT no cabeçalho.
- **Descrição**: Atualiza dados cadastrais de um usuário. Se a senha for enviada no corpo, ela será criptografada automaticamente antes de salvar.
- **Corpo da Requisição**: (Campos opcionais)
  ```json
  {
    "email": "novo_email@exemplo.com",
    "first_name": "NovoNome",
    "password": "nova_senha_secreta"
  }
  ```

#### Excluir Usuário
- **Endpoint**: `DELETE /auth/users/{user_id}`
- **Requisito**: Requer Token JWT no cabeçalho.
- **Descrição**: Remove permanentemente um usuário do sistema.

#### Obter Token (Login)
- **Endpoint**: `POST /auth/login`
- **Descrição**: Autentica o usuário e retorna o `access_token` e o `refresh_token`. Utilize o `access_token` no cabeçalho `Authorization`.
- **Corpo da Requisição (Form Data)**:
  - `username`: seu_email@exemplo.com
  - `password`: sua_senha
- **Resposta**:
  ```json
  {
    "access_token": "eyJhbG...",
    "refresh_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

#### Renovar Token (Refresh)
- **Endpoint**: `POST /auth/refresh`
- **Descrição**: Gera um novo `access_token` e um novo `refresh_token` sem a necessidade de reautenticar com e-mail e senha.
- **Parâmetro de Consulta**: `refresh_token` (o token recebido anteriormente no login ou refresh)

#### Como Usar o Token no Swagger
Para testar endpoints protegidos diretamente pelo Swagger UI:
1. Acesse `/docs`.
2. Clique no botão **Authorize** (topo da página).
3. Insira o seu Token JWT (recebido no login) no campo **Value** e clique em **Authorize**.
4. Todas as requisições subsequentes incluirão o cabeçalho `Authorization: Bearer <token>` automaticamente.

#### Como Usar o Token Manualmente
Adicione o token recebido no cabeçalho `Authorization` de todas as suas requisições subsequentes:
```text
Authorization: Bearer <seu_access_token_aqui>
```

---

### 2. Cadastro de Endereços (Clientes e Fornecedores)

O sistema foi projetado para que um **Cliente** ou **Fornecedor** possa ter múltiplos endereços. Por esse motivo, o cadastro é realizado em duas etapas.

#### Passo a Passo para Clientes

1.  **Criar o Cliente**: Primeiro, realize o cadastro do cliente para obter o seu `id`.
    -   **Endpoint**: `POST /customers/`
    -   **Payload**:
        ```json
        {
          "full_name": "João da Silva",
          "cpf": "123.456.789-00",
          "email": "joao@exemplo.com",
          "phone": "11988887777"
        }
        ```
    -   **Resposta**: Você receberá o objeto criado com um `"id": 1` (exemplo).

2.  **Vincular o Endereço**: Com o `id` em mãos, utilize o endpoint de endereços informando o `customer_id`.
    -   **Endpoint**: `POST /addresses/`
    -   **Payload**:
        ```json
        {
          "cep": "01001-000",
          "street": "Praça da Sé",
          "neighborhood": "Sé",
          "city": "São Paulo",
          "state": "SP",
          "number": "100",
          "customer_id": 1
        }
        ```

#### Passo a Passo para Fornecedores

1.  **Criar o Fornecedor**: Realize o cadastro para obter o `id` do fornecedor.
    -   **Endpoint**: `POST /suppliers/`
    -   **Payload**:
        ```json
        {
          "corporate_name": "Distribuidora de Teclados LTDA",
          "cnpj": "12.345.678/0001-90",
          "email": "vendas@distribuidora.com",
          "contact_name": "Roberto"
        }
        ```
    -   **Resposta**: Você receberá o objeto criado com um `"id": 5` (exemplo).

2.  **Vincular o Endereço**: Utilize o endpoint de endereços informando o `supplier_id`.
    -   **Endpoint**: `POST /addresses/`
    -   **Payload**:
        ```json
        {
          "cep": "01310-100",
          "street": "Avenida Paulista",
          "neighborhood": "Bela Vista",
          "city": "São Paulo",
          "state": "SP",
          "number": "1500",
          "supplier_id": 5
        }
        ```

#### 💡 Dica: Preenchimento Automático via CEP
Você pode consultar os dados de um endereço antes de cadastrá-lo usando o endpoint de integração com o ViaCEP:
- **Endpoint**: `GET /addresses/cep/{cep}`
- **Exemplo**: `GET /addresses/cep/01001000`
- **Retorno**: A API retornará `street`, `neighborhood`, `city` e `state` automaticamente, facilitando o preenchimento do seu payload de cadastro.

---

### 3. Outros Endpoints Principais

#### Clientes (Customers)
- `GET /customers/`: Lista todos os clientes. (Requer Token)
- `POST /customers/`: Cadastra um novo cliente. (Requer Token)
  ```json
  {
    "full_name": "Maria Oliveira",
    "cpf": "123.456.789-00",
    "email": "maria@exemplo.com",
    "phone": "11988887777"
  }
  ```

#### Produtos (Products)
- `GET /products/`: Lista todos os produtos. (Requer Token)
- `POST /products/`: Cria um novo produto. (Requer Token)
  ```json
  {
    "sku": "PROD001",
    "name": "Teclado Mecânico RGB",
    "description": "Teclado com switches blue e iluminação personalizável",
    "regular_price": 250.00,
    "discount_price": 220.00,
    "quantity": 50,
    "product_status_id": 1
  }
  ```

#### Endereços (Addresses)
A API valida o CEP e pode preencher automaticamente os campos de Logradouro, Bairro e Cidade através da integração com o ViaCEP. Para o processo completo de vinculação, veja a seção [Cadastro de Endereços](#2-cadastro-de-endereços-clientes-e-fornecedores).

- `POST /addresses/`: Vincula um endereço a um cliente ou fornecedor. (Requer Token)
  ```json
  {
    "cep": "01001-000",
    "street": "Praça da Sé",
    "neighborhood": "Sé",
    "city": "São Paulo",
    "state": "SP",
    "number": "100",
    "customer_id": 1
  }
  ```

#### Cupons (Coupons)
- `GET /coupons/`: Lista cupons ativos. (Requer Token)
- `POST /coupons/`: Cria um novo código de desconto. (Requer Token)

---

## 📦 Migrações com Alembic

O Alembic já está configurado para detectar automaticamente seus modelos em `app/models/models.py`.

### Comandos Principais (via Docker)

1. **Gerar uma nova migração**:
   Sempre que alterar seus modelos SQLAlchemy, execute:

   ```bash
   docker-compose exec app alembic revision --autogenerate -m "descricao_da_mudanca"
   ```
2. **Aplicar migrações**:
   Para atualizar o banco de dados com as últimas mudanças:

   ```bash

   docker-compose exec app alembic upgrade head
   ```
3. **Verificar status**:

   ```bash
   docker-compose exec app alembic current
   ```

### Execução Local (Fora do Docker)

Se preferir rodar o Alembic diretamente no seu terminal local (ex: no VS Code ou PowerShell), siga estes passos:

1. **Ative seu ambiente virtual e instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```
2. **Ajuste o arquivo `.env`**:
   O host do banco de dados deve ser `localhost` em vez de `db` (usado apenas dentro do Docker):
   `DATABASE_URL=postgresql://gmontinny:Gmontinny2026@localhost:5432/db`
3. **Garanta que o banco de dados está rodando no Docker**:

   ```bash
   docker-compose up -d db
   ```
4. **Execute os comandos diretamente**:

   - `alembic revision --autogenerate -m "sua_descricao"`
   - `alembic upgrade head`
   - `alembic current`

### Configuração Técnica

- O arquivo `alembic/env.py` foi configurado para importar o `Base.metadata` de `app.db.session` e carregar os modelos de `app.models`.
- A URL do banco de dados é lida automaticamente do seu arquivo `.env` através das configurações do Pydantic.
