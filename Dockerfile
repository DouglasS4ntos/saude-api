FROM python:3.13-slim

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependências do sistema para o Psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install poetry

# Copia arquivos de dependência
COPY pyproject.toml poetry.lock /app/

# Configura o poetry para não criar virtualenv dentro do container
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copia o restante do projeto
COPY . /app/

EXPOSE 8000
