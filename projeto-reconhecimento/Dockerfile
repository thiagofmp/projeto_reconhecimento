# Usa uma imagem oficial do Python mais enxuta
FROM python:3.10-slim

# Instala dependências básicas do sistema necessárias para o OpenCV rodar no Linux
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app:app"]