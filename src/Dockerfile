# Imagem base do Python
FROM python:3.10-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY src ./src

# Expor a porta que a aplicação irá rodar para fora do container
EXPOSE 8000

# Comando para iniciar o servidor após inicio do container
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
