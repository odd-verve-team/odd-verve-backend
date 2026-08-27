# Використовуємо офіційний мінімальний образ Python 3.11
FROM python:3.11-slim

# Запобігаємо запису .pyc файлів та вмикаємо миттєвий вивід логів у консоль
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Встановлюємо системні залежності для збірки psycopg2 та інших пакетів C-level
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо вихідний код проєкту
COPY . /app/

# Створюємо директорії для статики та медіафайлів
RUN mkdir -p /app/staticfiles /app/media

# Відкриваємо порт 8000
EXPOSE 8000

# Команда за замовчуванням для запуску продуктового сервера Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]