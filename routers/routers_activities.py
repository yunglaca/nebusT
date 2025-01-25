from fastapi import APIRouter, Depends
from db.database import db_dependency
from crud.cruds_activities import get_activities
from schemas.activity_schemas import ActivitySchema
from typing import List
from utils.api_key_validation import verify_api_key

router = APIRouter()


# Список всех видов деятельности
@router.get("/activities", response_model=List[ActivitySchema])
async def get_activities_route(db: db_dependency, _: None = Depends(verify_api_key)):
    return await get_activities(db)
