# personal-ai-manager/docker/app.Dockerfile

# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação (será sobreposto pelo volume no dev)
COPY ./src .

# Expõe a porta que a aplicação vai rodar
EXPOSE 8000