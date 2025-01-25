#!/bin/sh
sleep 10

echo "Executing database migrations..."

# Формируем URL для подключения к базе данных
DATABASE_URL="postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

# Экспортируем переменную окружения для Alembic
export DATABASE_URL

# Запускаем миграции Alembic
alembic upgrade head
# Проверяем успешность выполнения миграций
if [ $? -ne 0 ]; then
    echo "Migrations failed. Exiting."
    exit 1
fi

echo "Migrations succeeded. Adding test data..."

# Добавляем тестовые данные в базу данных через psql
psql $DATABASE_URL <<EOF
-- Добавление тестовых данных для таблицы buildings
INSERT INTO buildings (id, address, latitude, longitude) VALUES
(1, 'г. Москва, ул. Ленина, 1', 55.7558, 37.6173),
(2, 'г. Санкт-Петербург, ул. Невский, 15', 59.9343, 30.3351);

-- Добавление тестовых данных для таблицы activitys
INSERT INTO activitys (id, name, parent_id) VALUES
(1, 'Еда', NULL),
(2, 'Мясная продукция', 1),
(3, 'Молочная продукция', 1),
(4, 'Автомобили', NULL),
(5, 'Грузовые', 4);

-- Добавление тестовых данных для таблицы organizations
INSERT INTO organizations (id, name, phone_numbers, building_id) VALUES
(1, 'ООО Рога и Копыта', '{"8-800-555-35-35", "2-222-222"}', 1),
(2, 'ИП МясоЕда', '{"3-333-333"}', 2);

-- Добавление тестовых данных для связи organization_activity
INSERT INTO organization_activity (organization_id, activity_id) VALUES
(1, 1),  -- ООО Рога и Копыта занимается Едой
(1, 2),  -- ООО Рога и Копыта занимается Мясной продукцией
(2, 3);  -- ИП МясоЕда занимается Молочной продукцией
EOF

# Проверка успешности добавления тестовых данных
if [ $? -ne 0 ]; then
    echo "Adding test data failed. Exiting."
    exit 1
fi

echo "Test data added successfully."

echo "Starting the application..."

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
