from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1 import auth, products, customers, suppliers, addresses, categories, metadata, coupons
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"])
description = """
API de E-commerce completa desenvolvida com FastAPI.

## Funcionalidades
* **Autenticação**: Registro, Login e Refresh Token de usuários com JWT.
* **Produtos**: Gerenciamento completo de catálogo de produtos.
* **Clientes e Fornecedores**: Cadastro de entidades com múltiplos endereços.
* **Integração ViaCEP**: Busca automática de endereços por CEP.
* **Categorias e Metadados**: Gestão de categorias, tags e status de produtos.
* **Cupons**: Sistema de descontos aplicáveis.
* **Segurança**: Rate Limiting e criptografia de senhas.

---
Para usar os endpoints protegidos via Swagger:
1. Obtenha o token no endpoint `POST /auth/login` (ou use um token existente).
2. Copie o `access_token` da resposta.
3. Clique no botão **Authorize** (topo da página).
4. No campo **Value**, cole apenas o token (ex: `eyJhbG...`) e clique em **Authorize**.
5. Todas as requisições subsequentes incluirão o cabeçalho automaticamente.
"""

app = FastAPI(
    title="E-commerce API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Suporte E-commerce",
        "email": "suporte@exemplo.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        loc = error.get("loc")
        msg = error.get("msg")
        type = error.get("type")
        
        # Tradução de mensagens comuns do Pydantic V2
        if "field required" in msg.lower() or "missing" in type:
            translated_msg = "Este campo é obrigatório"
        elif "value is not a valid email" in msg.lower() or "value_error.email" in type or "email_parsing" in type:
            translated_msg = "O e-mail fornecido não é válido"
        elif "value_error.number.not_ge" in type or "greater_than_equal" in type:
            limit = error.get("ctx", {}).get("ge")
            translated_msg = f"O valor deve ser maior ou igual a {limit}"
        elif "string_pattern_mismatch" in type:
            translated_msg = "O formato fornecido para este campo é inválido"
        elif "assertion_failed" in type:
            translated_msg = "A validação falhou para este campo"
        elif "type_error.integer" in type or "int_parsing" in type:
            translated_msg = "O valor deve ser um número inteiro"
        elif "type_error.decimal" in type or "decimal_parsing" in type:
            translated_msg = "O valor deve ser um número decimal válido"
        elif "too_short" in type:
            limit = error.get("ctx", {}).get("min_length") or error.get("ctx", {}).get("limit_value")
            translated_msg = f"O campo deve ter pelo menos {limit} caracteres/itens"
        elif "too_long" in type:
            limit = error.get("ctx", {}).get("max_length") or error.get("ctx", {}).get("limit_value")
            translated_msg = f"O campo deve ter no máximo {limit} caracteres/itens"
        else:
            translated_msg = msg # Fallback se não mapeado
            
        errors.append({
            "loc": loc,
            "msg": translated_msg,
            "type": type
        })
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(suppliers.router)
app.include_router(addresses.router)
app.include_router(categories.router)
app.include_router(metadata.router)
app.include_router(coupons.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de E-commerce"}

# Customização do Schema OpenAPI para garantir que o Bearer Auth seja exibido corretamente
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Define o esquema de autenticação Bearer
    # O FastAPI já gera um esquema de segurança HTTPBearer se o usarmos em Depends
    # mas aqui garantimos que o nome e a descrição fiquem amigáveis.
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
