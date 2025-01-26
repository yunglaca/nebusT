# nebusT
test task 


## Как запустить

1) заполнить .env по примеру .env.example
2) docker-compose up --build


### Тестирование эндпоинтов происходит в автосвагере

заходим на хост/docs (в терминале) и жмякаем на эндпоинты


#### Описаие эндпоинтов

Деятельность:

Получение всех видов деятельности
```bash
GET http://localhost:8000/activitys
X-API-KEY: your-api-key-here

[
    {
        "id": 1,
        "name": "Еда",
        "parent_id": null
    },
    {
        "id": 2,
        "name": "Мясная продукция",
        "parent_id": 1
    },
    {
        "id": 3,
        "name": "Молочная продукция",
        "parent_id": 1
    },
    {
        "id": 4,
        "name": "Автомобили",
        "parent_id": null
    }
]
```

Здания:

Получение всех зданий

```bash
GET http://localhost:8000/buildings
X-API-KEY: your-api-key-here
пример ответа:
[
    {
        "id": 1,
        "address": "г. Москва, ул. Ленина, 1",
        "latitude": 55.7558,
        "longitude": 37.6173
    },
    {
        "id": 2,
        "address": "г. Санкт-Петербург, ул. Невский, 15",
        "latitude": 59.9343,
        "longitude": 30.3351
    }
]
```

Организации:

1. Получение организаций по зданию

```bash
GET http://localhost:8000/organizations/1
X-API-KEY: your-api-key-here

Пример ответа

[
    {
        "id": 1,
        "name": "ООО Рога и Копыта",
        "phone_numbers": ["8-800-555-35-35", "2-222-222"],
        "building_id": 1
    },
    {
        "id": 2,
        "name": "ИП МясоЕда",
        "phone_numbers": ["3-333-333"],
        "building_id": 1
    }
]
```

2. Список организаций, относящихся к виду деятельности

```bash
GET http://localhost:8000/activities/1/organizations
X-API-KEY: your-api-key-here

Пример ответа:

[
    {
        "id": 1,
        "name": "ООО Рога и Копыта",
        "phone_numbers": ["8-800-555-35-35", "2-222-222"],
        "building_id": 1
    },
    {
        "id": 3,
        "name": "ИП Молочные Продукты",
        "phone_numbers": ["4-444-444"],
        "building_id": 2
    }
]

```

3. Вывод информации об организации по её идентификатору

```bash
GET http://localhost:8000/organizations/1
X-API-KEY: your-api-key-here

Пример ответа:

{
    "id": 1,
    "name": "ООО Рога и Копыта",
    "phone_numbers": ["8-800-555-35-35", "2-222-222"],
    "building_id": 1
}
```

4. Поиск организации по названию

```bash
GET http://localhost:8000/organizations/search/name?name=Рога
X-API-KEY: your-api-key-here

ПРимер ответа

[
    {
        "id": 1,
        "name": "ООО Рога и Копыта",
        "phone_numbers": ["8-800-555-35-35", "2-222-222"],
        "building_id": 1
    }
]

```

5. Поиск организаций по виду деятельности
```bash
GET http://localhost:8000/organizations/search/activity?activity_name=Еда
X-API-KEY: your-api-key-here

Пример ответа:

{
    "id": 1,
    "name": "ООО Рога и Копыта",
    "phone_numbers": ["8-800-555-35-35", "2-222-222"],
    "building_id": 1
}

```

6. Поиск организаций и зданий в прямоугольной области
```bash
GET http://localhost:8000/organizations_and_buildings_in_area?min_lat=55.0&max_lat=56.0&min_lon=37.0&max_lon=38.0
X-API-KEY: your-api-key-here

Пример ответа:
{
    "buildings": [
        {
            "id": 1,
            "address": "г. Москва, ул. Ленина, 1",
            "latitude": 55.7558,
            "longitude": 37.6173
        },
        {
            "id": 2,
            "address": "г. Санкт-Петербург, ул. Невский, 15",
            "latitude": 59.9343,
            "longitude": 30.3351
        }
    ],
    "organizations": [
        {
            "id": 1,
            "name": "ООО Рога и Копыта",
            "phone_numbers": ["8-800-555-35-35", "2-222-222"],
            "building_id": 1
        },
        {
            "id": 2,
            "name": "ИП МясоЕда",
            "phone_numbers": ["3-333-333"],
            "building_id": 1
        }
    ]
}

```