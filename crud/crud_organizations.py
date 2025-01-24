from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from db.models import Organization, Activity


# Функция для создания организации
async def create_organization(
    session: AsyncSession, name: str, phone_numbers: List[str], building_id: int, activity_ids: List[int]
) -> Organization:
    organization = Organization(name=name, phone_numbers=phone_numbers, building_id=building_id)
    session.add(organization)
    await session.commit()
    await session.refresh(organization)
    
    for activity_id in activity_ids:
        activity = await session.get(Activity, activity_id)
        if activity:
            organization.activities.append(activity)
    
    await session.commit()
    return organization


# Функция для получения всех организаций
async def get_all_organizations(session: AsyncSession) -> List[Organization]:
    result = await session.execute(select(Organization).options(selectinload(Organization.building), selectinload(Organization.activities)))
    organizations = result.scalars().all()
    return organizations


# Функция для поиска организации по названию
async def search_organization_by_name(session: AsyncSession, name: str) -> List[Organization]:
    result = await session.execute(select(Organization).filter(Organization.name.ilike(f"%{name}%")))
    organizations = result.scalars().all()
    return organizations
