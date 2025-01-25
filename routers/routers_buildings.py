from fastapi import APIRouter
from db.database import db_dependency
from crud.cruds_buildings import get_buildings
from typing import List
from schemas.builduing_schemas import Building
router = APIRouter()

# 1. Список всех зданий
@router.get("/buildings", response_model=List[Building])
async def get_buildings_route(db: db_dependency):
    return await get_buildings(db)
