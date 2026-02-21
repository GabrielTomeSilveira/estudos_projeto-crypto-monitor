# Usa a imagem oficial do Python 3.13 (versão slim para reduzir tamanho)
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (aproveita cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código fonte
COPY . .

# Define o comando padrão: executar o pipeline
CMD ["python", "main.py"]