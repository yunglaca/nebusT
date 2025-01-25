from pydantic import BaseModel
from schemas.activity_schemas import ActivitySchema
from schemas.builduing_schemas import BuildingSchema
from typing import List


# Схема для Organization (для отображения данных)
class OrganizationInDB(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]
    building: BuildingSchema
    activities: List[ActivitySchema] = []

    class Config:
        from_attributes = True


# Схема для поиска организаций по названию
class OrganizationSearchResult(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Схема для поиска организаций по виду деятельности
class OrganizationSearchByActivityResult(BaseModel):
    id: int
    name: str
    activities: List[ActivitySchema] = []

    class Config:
        from_attributes = True
