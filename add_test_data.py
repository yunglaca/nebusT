from db.database import async_session_maker
from db.models import Building, Activity, Organization, organization_activity
from sqlalchemy import insert

async def add_test_data():
    async with async_session_maker() as session:
        try:
            # Добавление данных в таблицу buildings
            buildings = [
                Building(address="г. Москва, ул. Ленина, 1", latitude=55.7558, longitude=37.6173),
                Building(address="г. Санкт-Петербург, ул. Невский, 15", latitude=59.9343, longitude=30.3351),
            ]
            session.add_all(buildings)

            # Добавление данных в таблицу activities
            activities = [
                Activity(name="Еда", parent_id=None),
                Activity(name="Мясная продукция", parent_id=1),
                Activity(name="Молочная продукция", parent_id=1),
                Activity(name="Автомобили", parent_id=None),
                Activity(name="Грузовые", parent_id=4),
            ]
            session.add_all(activities)

            # Добавление данных в таблицу organizations
            organizations = [
                Organization(name="ООО Рога и Копыта", phone_numbers=["8-800-555-35-35", "2-222-222"], building_id=1),
                Organization(name="ИП МясоЕда", phone_numbers=["3-333-333"], building_id=2),
            ]
            session.add_all(organizations)

            # Сохраняем изменения в базе данных
            await session.commit()

            # Добавление данных в таблицу связи organization_activity вручную
            # Для этого используем insert() для явного добавления записей в таблицу связи
            stmt = insert(organization_activity).values([
                {"organization_id": 1, "activity_id": 1},
                {"organization_id": 1, "activity_id": 2},
                {"organization_id": 2, "activity_id": 3},
            ])
            await session.execute(stmt)
            
            # Сохраняем изменения в базе данных
            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"Error adding test data: {e}")


# Вызов функции при запуске скрипта
if __name__ == "__main__":
    import asyncio
    asyncio.run(add_test_data())
