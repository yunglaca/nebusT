from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import Activity
from schemas.activity_schemas import ActivitySchema 

async def get_activities(db: AsyncSession):
    query = select(Activity).options(
        selectinload(Activity.children)
    ) 
    async with db.begin():
        result = await db.execute(query)
    activities = result.scalars().all()

    return [ActivitySchema.from_orm(activity) for activity in activities]
