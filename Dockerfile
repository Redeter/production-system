# Этап 1: Сборка фронтенда
FROM node:16-alpine as frontend-build

WORKDIR /app/frontend

# Копируем package.json сначала для кэширования зависимостей
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Копируем исходный код и собираем
COPY frontend/ .
RUN npm run build

# Этап 2: Финальный образ
FROM python:3.9-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бэкенда
COPY backend/ .

# Копируем собранный фронтенд из первого этапа
COPY --from=frontend-build /app/frontend/build ./static

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]