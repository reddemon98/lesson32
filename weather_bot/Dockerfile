# Используйте официальный Python образ
FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте зависимости
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте весь проект
COPY . .

# Задайте команду для запуска приложения
CMD ["python", "bot.py"]
