from fastapi import APIRouter,Depends
from db.database import db_dependency
from crud.cruds_buildings import get_buildings
from typing import List
from schemas.builduing_schemas import Building
from utils.api_key_validation import verify_api_key
router = APIRouter()

# 1. Список всех зданий
@router.get("/buildings", response_model=List[Building])
async def get_buildings_route(db: db_dependency,_: None = Depends(verify_api_key)):
    return await get_buildings(db)
