from fastapi import APIRouter
from db.database import db_dependency
from crud.cruds_buildings import create_building, get_all_buildings
from schemas.schemas_app import BuildingCreate, BuildingOut
from typing import List

router = APIRouter()

# Роуты для зданий
@router.post("/", response_model=BuildingOut)
async def create_new_building(building: BuildingCreate, db: db_dependency):
    return await create_building(db, building.address, building.latitude, building.longitude)


@router.get("/", response_model=List[BuildingOut])
async def get_buildings(db: db_dependency):
    return await get_all_buildings(db)
