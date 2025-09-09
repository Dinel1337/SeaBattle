#!/bin/bash

set -e  # Выход при ошибке

# Параметры из переменных окружения (или значения по умолчанию)
DB_USER="${POSTGRES_USER:-dinelore}"
DB_PASS="${POSTGRES_PASSWORD:-dinelefox}"
DB_NAME="${POSTGRES_DB:-mydatabase}"

# Функция для проверки существования пользователя
user_exists() {
    sudo -u postgres psql -tAc "SELECT 1 FROM pg_user WHERE usename='$DB_USER'" | grep -q 1
}

# Функция для проверки существования БД
db_exists() {
    sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1
}

# Создаём пользователя, если его нет
if ! user_exists; then
    echo "🔄 Создаём пользователя PostgreSQL: $DB_USER"
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
else
    echo "ℹ️ Пользователь $DB_USER уже существует"
fi

# Создаём БД, если её нет
if ! db_exists; then
    echo "🔄 Создаём БД: $DB_NAME"
    sudo -u postgres createdb -O "$DB_USER" "$DB_NAME"
    sudo -u postgres psql -d "$DB_NAME" -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
else
    echo "ℹ️ БД $DB_NAME уже существует"
fi

# Запуск приложения
echo "🚀 Запуск FastAPI..."
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload