FROM python:3.12-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Instalar dependências de sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos de dependências primeiro (aproveitamento de cache)
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para o container
COPY . .

# Expor a porta que o FastAPI utilizará
EXPOSE 8000

# Comando para rodar a aplicação usando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
