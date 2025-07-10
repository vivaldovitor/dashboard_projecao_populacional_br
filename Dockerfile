FROM python:3.11-slim

WORKDIR /app
COPY . ./

# Atualize pacotes do sistema e limpe cache
RUN apt-get update && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crie e use um usuário não-root
RUN useradd -m appuser
USER appuser

EXPOSE 8080

CMD ["python", "index.py"]