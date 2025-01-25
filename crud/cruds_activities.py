from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import Activity  # Импортируем модель SQLAlchemy
from schemas.activity_schemas import ActivitySchema # Импортируем схему Pydantic

async def get_activities(db: AsyncSession):
    # Пример запроса с асинхронной сессией и загрузкой связанных объектов
    query = select(Activity).options(selectinload(Activity.children))  # Загрузка связанных детей
    async with db.begin():
        result = await db.execute(query)
    activities = result.scalars().all()

    return [ActivitySchema.from_orm(activity) for activity in activities]
