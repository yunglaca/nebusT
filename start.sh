#!/bin/sh
sleep 10

echo "Executing database migrations..."


# Применяем миграции до последней версии
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "Migrations failed. Exiting."
    exit 1
fi

echo "Migrations succeeded. Adding test data..."

# Запускаем добавление тестовых данных
python3 add_test_data.py
if [ $? -ne 0 ]; then
    echo "Adding test data failed. Exiting."
    exit 1
fi

echo "Test data added successfully. Starting the application..."

# Запускаем приложение
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
