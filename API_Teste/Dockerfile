FROM python:3.9-slim

# Instala dependências de sistema necessárias para mysqlclient e netcat
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Copia o script de entrada e dá permissão de execução
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expõe a porta padrão do Django
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]