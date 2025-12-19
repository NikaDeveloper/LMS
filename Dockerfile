# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное из текущей папки в контейнер
COPY . .

# Команда, которая запускается по умолчанию (запуск сервера)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
