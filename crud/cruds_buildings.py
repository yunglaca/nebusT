from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Building
from typing import List


# Функция для создания нового здания
async def create_building(session: AsyncSession, address: str, latitude: float, longitude: float) -> Building:
    building = Building(address=address, latitude=latitude, longitude=longitude)
    session.add(building)
    await session.commit()
    await session.refresh(building)
    return building


# Функция для получения всех зданий
async def get_all_buildings(session: AsyncSession) -> List[Building]:
    result = await session.execute(select(Building))
    buildings = result.scalars().all()
    return buildings
