# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app/app

# Define o PYTHONPATH para que os módulos sejam encontrados
ENV PYTHONPATH=/app

# Comando corrigido para encontrar o app a partir da subpasta 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]