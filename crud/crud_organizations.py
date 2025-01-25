from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Organization, Activity, organization_activity
from schemas.organizations_schemas import OrganizationInDB
from sqlalchemy.orm import selectinload, joinedload

# 1 Функция для получения организаций по зданию
async def get_organizations_by_building(building_id: int, db: AsyncSession):
    query = select(Organization).filter(Organization.building_id == building_id)
    result = await db.execute(query)
    organizations = result.scalars().all()
    return organizations

# 2. Получение организаций по виду деятельности  без дочерних

async def get_organizations_by_activity(activity_id: int, db: AsyncSession):
    # Запрос на поиск организаций по основной деятельности
    query = select(Organization).join(organization_activity).filter(organization_activity.c.activity_id == activity_id).options(
        selectinload(Organization.building),
        selectinload(Organization.activities)
    )
    async with db.begin():
        result = await db.execute(query)
    
    organizations = result.scalars().all()

    return [OrganizationInDB.from_orm(org) for org in organizations]


# 3. Получение организации по ID
async def get_organization_by_id(organization_id: int, db: AsyncSession):
    result = await db.execute(select(Organization).filter(Organization.id == organization_id))
    return result.scalars().first()

# 4. Поиск организаций по названию
async def search_organizations_by_name(name: str, db: AsyncSession):
    result = await db.execute(select(Organization).filter(Organization.name.ilike(f"%{name}%")))
    return result.scalars().all()

# 5. Поиск организаций по названию деятельности включая дочерние
async def get_organizations_by_activity_name(activity_name: str, db: AsyncSession):
    # Шаг 1: Получаем основную активность с загрузкой всех её связанных сущностей через selectinload
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
        # Шаг 2: Собираем все связанные активности (дети, внуки и т.д.)
        activity_ids = [activity.id]
        
        # добавляем все дочерние активности на всех уровнях
        def collect_activity_ids(activity):
            activity_ids.append(activity.id)
            for child in activity.children:
                collect_activity_ids(child)
        
        collect_activity_ids(activity)

        # Шаг 3: Получаем организации, связанные с активностями
        query = select(Organization).join(organization_activity).filter(
            organization_activity.c.activity_id.in_(activity_ids)
        ).options(
            selectinload(Organization.building),  
            selectinload(Organization.activities)
        )

        result = await db.execute(query)
        organizations = result.scalars().all()  # Получаем все организации

        # Возвращаем организации в формате, который нам нужен
        return [OrganizationInDB.from_orm(org) for org in organizations]
    
    return []  # если нету, то пустой лист