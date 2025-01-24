from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Activity
from typing import List


# Функция для создания активности
async def create_activity(session: AsyncSession, name: str, parent_id: int = None):
    if parent_id and parent_id not in [1, 2, 3]:
        raise ValueError("parent_id должен быть числом от 1 до 3")
    
    new_activity = Activity(name=name, parent_id=parent_id)
    session.add(new_activity)
    await session.commit()
    return new_activity


# Функция для получения всех видов деятельности
async def get_all_activities(session: AsyncSession) -> List[Activity]:
    result = await session.execute(select(Activity))
    activities = result.scalars().all()
    return activities
