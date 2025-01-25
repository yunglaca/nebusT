from db.database import async_session_maker
from db.models import Building, Activity, Organization, organization_activity


async def add_test_data():
    async with async_session_maker() as session:
        try:
            # Добавление данных в таблицу buildings
            buildings = [
                Building(address="г. Москва, ул. Ленина, 1", latitude=55.7558, longitude=37.6173),
                Building(address="г. Санкт-Петербург, ул. Невский, 15", latitude=59.9343, longitude=30.3351),
            ]
            session.add_all(buildings)

            # Добавление данных в таблицу activitys
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

            # Добавление данных в таблицу organization_activity
            org_activities = [
                organization_activity(organization_id=1, activity_id=1),
                organization_activity(organization_id=1, activity_id=2),
                organization_activity(organization_id=2, activity_id=3),
            ]
            session.add_all(org_activities)

            # Сохраняем изменения в базе данных
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Error adding test data: {e}")


# Вызов функции при запуске скрипта
if __name__ == "__main__":
    import asyncio
    asyncio.run(add_test_data())
