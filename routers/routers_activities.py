from fastapi import APIRouter
from db.database import db_dependency
from crud.cruds_activities import create_activity, get_all_activities
from schemas.schemas_app import ActivityCreate, ActivityOut
from typing import List

router = APIRouter()

# Роуты для деятельностей
@router.post("/", response_model=ActivityOut)
async def create_new_activity(db: db_dependency, activity: ActivityCreate):
    return await create_activity(db, activity.name)


@router.get("/", response_model=List[ActivityOut])
async def get_activities(db: db_dependency):
    return await get_all_activities(db)
