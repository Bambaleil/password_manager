#!/bin/bash

echo "Останавливаем и удаляем контейнеры..."
docker-compose down

echo "Удаляем старый образ..."
docker image rm backend:latest || true

echo "Очищаем неиспользуемые данные Docker..."
docker system prune -f

echo "Собираем образы..."
docker-compose build --no-cache

echo "Запускаем контейнеры..."
docker-compose up -d

echo "Готово!"
