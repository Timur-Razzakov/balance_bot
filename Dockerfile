FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Системные зависимости
RUN apt-get update && \
    apt-get install -y \
        vim \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 1️⃣ Копируем ТОЛЬКО requirements.txt
COPY requirements.txt .

# 2️⃣ Устанавливаем зависимости (кешируется)
RUN pip install --no-cache-dir -r requirements.txt

# 3️⃣ Копируем остальной код
COPY . .

RUN chmod +x /app/startup.sh

CMD ["/app/startup.sh"]
