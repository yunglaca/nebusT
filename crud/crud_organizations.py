from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Organization, Activity, organization_activity,Building
from schemas.organizations_schemas import OrganizationInDB
from sqlalchemy.orm import selectinload
from schemas.builduing_schemas import BuildingSchema

# 1 Функция для получения организаций по зданию
async def get_organizations_by_building(building_id: int, db: AsyncSession):
    query = select(Organization).filter(Organization.building_id == building_id)
    result = await db.execute(query)
    organizations = result.scalars().all()
    return organizations


# 2. Получение организаций по виду деятельности  без дочерних
async def get_organizations_by_activity(activity_id: int, db: AsyncSession):
    query = (
        select(Organization)
        .join(organization_activity)
        .filter(organization_activity.c.activity_id == activity_id)
        .options(
            selectinload(Organization.building), selectinload(Organization.activities)
        )
    )
    async with db.begin():
        result = await db.execute(query)

    organizations = result.scalars().all()

    return [OrganizationInDB.from_orm(org) for org in organizations]


# 3. Получение организации по ID
async def get_organization_by_id(organization_id: int, db: AsyncSession):
    result = await db.execute(
        select(Organization).filter(Organization.id == organization_id)
    )
    return result.scalars().first()


# 4. Поиск организаций по названию
async def search_organizations_by_name(name: str, db: AsyncSession):
    result = await db.execute(
        select(Organization).filter(Organization.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()


# 5. Поиск организаций по названию деятельности включая дочерние
async def get_organizations_by_activity_name(activity_name: str, db: AsyncSession):
    result = await db.execute(
        select(Activity)
        .filter(Activity.name == activity_name)
        .options(
            selectinload(Activity.children)  # Загружаем первый уровень и так до 3
            .selectinload(Activity.children)  # (2)
            .selectinload(Activity.children)  # (3)
        )
    )

    activity = result.scalars().first()  # Получаем первую найденную активность

    if activity:
        activity_ids = [activity.id]

        # добавляем все дочерние активности на всех уровнях
        def collect_activity_ids(activity):
            activity_ids.append(activity.id)
            for child in activity.children:
                collect_activity_ids(child)

        collect_activity_ids(activity)
        query = (
            select(Organization)
            .join(organization_activity)
            .filter(organization_activity.c.activity_id.in_(activity_ids))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
            )
        )

        result = await db.execute(query)
        organizations = result.scalars().all()

        return [OrganizationInDB.from_orm(org) for org in organizations]

    return []  # если нету, то пустой лист
#6 по области   (квадрат)
async def get_organizations_and_buildings_in_area(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    db: AsyncSession
):
    """
    Функция для получения зданий и организаций в прямоугольной области
    относительно заданных координат.
    """
    # Формирование запроса для получения зданий
    query = select(Building).filter(
        Building.latitude >= min_lat,
        Building.latitude <= max_lat,
        Building.longitude >= min_lon,
        Building.longitude <= max_lon
    )

    # Выполнение запроса для получения зданий
    buildings = (await db.execute(query)).scalars().all()

    # Получаем список организаций, привязанных к зданиям
    building_ids = [building.id for building in buildings]
    organizations_query = select(Organization).filter(Organization.building_id.in_(building_ids))
    organizations = (await db.execute(organizations_query)).scalars().all()

    # Преобразование моделей SQLAlchemy в Pydantic схемы
    building_models = [BuildingSchema.from_orm(building) for building in buildings]
    organization_models = [OrganizationInDB.from_orm(org) for org in organizations]

    # Формируем результат
    return {
        "buildings": building_models,
        "organizations": organization_models,
    }