#!/bin/bash

set -e

CONTAINER_NAME="sea"
IMAGE_NAME="api"
PORT="8000"
VOLUME_MAPPING="$(pwd)/backend:/app/backend"

echo "🔄 Рестарт контейнера $CONTAINER_NAME..."

if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "🔪 Останавливаем $CONTAINER_NAME..."
    docker kill $CONTAINER_NAME 2>/dev/null || echo "Контейнер не запущен, пропускаем kill"
    
    echo "🗑️ Удаляем $CONTAINER_NAME..."
    docker rm -f $CONTAINER_NAME || { echo "❌ Не удалось удалить $CONTAINER_NAME"; exit 1; }
else
    echo "ℹ️ Контейнер $CONTAINER_NAME не найден, пропускаем удаление"
fi

if [ -f "Dockerfile" ]; then
    echo "🛠️ Собираем образ $IMAGE_NAME..."
    docker build -t $IMAGE_NAME . || { echo "❌ Ошибка сборки образа"; exit 1; }
else
    echo "ℹ️ Dockerfile не найден, используем существующий образ $IMAGE_NAME"
fi

# Запускаем контейнер с твоими параметрами
echo "🚀 Запускаем $CONTAINER_NAME с volume и портом $PORT..."
docker run -d \
    --name $CONTAINER_NAME \
    -p $PORT:8000 \
    -v $VOLUME_MAPPING \
    $IMAGE_NAME || { echo "❌ Не удалось запустить $CONTAINER_NAME"; exit 1; }

echo "✅ Готово! Контейнер $CONTAINER_NAME запущен:"
docker ps --filter "name=$CONTAINER_NAME" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"