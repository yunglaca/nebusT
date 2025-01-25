from fastapi import APIRouter, HTTPException, Depends
from typing import List
from crud.crud_organizations import (
    get_organizations_by_building,
    get_organizations_by_activity,
    get_organization_by_id,
    search_organizations_by_name,
    get_organizations_by_activity_name,
)
from schemas.organizations_schemas import OrganizationInDB, OrganizationSearchResult, OrganizationSearchByActivityResult
from db.database import db_dependency
from utils.api_key_validation import verify_api_key

router = APIRouter()

# 1. Получение огранизации по зданию
@router.get("/organizations/{building_id}")
async def get_organizations(
    building_id: int, db: db_dependency, _: None = Depends(verify_api_key)
):
    organizations = await get_organizations_by_building(building_id, db)
    if not organizations:
        raise HTTPException(status_code=404, detail=f"error with {building_id}")
    return organizations


# 2. Список организаций, относящихся к виду деятельности
@router.get(
    "/activities/{activity_id}/organizations", response_model=List[OrganizationInDB]
)
async def get_organizations_by_activity_route(
    activity_id: int, db: db_dependency, _: None = Depends(verify_api_key)
):
    return await get_organizations_by_activity(activity_id, db)


# 3. Вывод информации об организации по её идентификатору
@router.get("/organizations/{organization_id}", response_model=OrganizationInDB)
async def get_organization_by_id_route(
    organization_id: int, db: db_dependency, _: None = Depends(verify_api_key)
):
    return await get_organization_by_id(organization_id, db)


# 4. Поиск организации по названию
@router.get("/organizations/search/name", response_model=List[OrganizationSearchResult])
async def search_organizations_by_name_route(
    name: str, db: db_dependency, _: None = Depends(verify_api_key)
):
    return await search_organizations_by_name(name, db)


# 5. Поиск организаций по виду деятельности
@router.get(
    "/organizations/search/activity",
    response_model=List[OrganizationSearchByActivityResult],
)
async def search_organizations_by_activity_route(
    activity_name: str, db: db_dependency, _: None = Depends(verify_api_key)
):
    return await get_organizations_by_activity_name(activity_name, db)
