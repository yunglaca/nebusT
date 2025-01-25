from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Building


# Получение всех зданий
async def get_buildings(db: AsyncSession):
    result = await db.execute(select(Building))
    return result.scalars().all()
