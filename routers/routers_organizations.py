from fastapi import APIRouter
from db.database import db_dependency
from crud.crud_organizations import create_organization, get_all_organizations, search_organization_by_name
from schemas.schemas_app import OrganizationCreate, OrganizationOut
from typing import List

router = APIRouter()

# Роуты для организаций
@router.post("/", response_model=OrganizationOut)
async def create_new_organization(organization: OrganizationCreate, db: db_dependency):
    return await create_organization(db, organization.name, organization.phone_numbers, organization.building_id, organization.activity_ids)


@router.get("/", response_model=List[OrganizationOut])
async def get_organizations(db: db_dependency):
    return await get_all_organizations(db)


@router.get("/search", response_model=List[OrganizationOut])
async def search_organizations(name: str, db: db_dependency):
    return await search_organization_by_name(db, name)
