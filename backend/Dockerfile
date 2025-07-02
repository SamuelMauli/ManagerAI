# Use uma imagem oficial do Python como imagem pai
FROM python:3.9-slim

# Define variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala as dependências primeiro para aproveitar o cache do Docker
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da pasta backend para o diretório /app do contêiner
COPY . .

# Define o comando para executar a aplicação
# A flag --app-dir diz ao Uvicorn para adicionar o diretório 'src' ao caminho do Python
CMD ["uvicorn", "app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000", "--reload"]