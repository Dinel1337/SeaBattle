FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Только для разработки - оставляем пустую директорию
RUN mkdir -p /app/backend

# Указываем рабочую директорию для приложения
WORKDIR /app/backend

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]