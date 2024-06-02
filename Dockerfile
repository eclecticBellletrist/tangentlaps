# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /bot

# Копируем файл зависимостей
COPY bot/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы бота в контейнер
COPY bot/ .

# Указываем команду для запуска вашего бота
CMD ["python", "main.py"]
